"""
Freight Rate Prediction Model
This script trains a machine learning model to predict freight rates.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Load data
print("Loading data...")
train_df = pd.read_csv('train-test.csv')
validation_df = pd.read_csv('validation.csv')
december_df = pd.read_csv('december-chart-inputs.csv')

print(f"Training data shape: {train_df.shape}")
print(f"Validation data shape: {validation_df.shape}")
print(f"December data shape: {december_df.shape}")

# Display sample data
print("\nTraining data sample:")
print(train_df.head())

print("\nData types:")
print(train_df.dtypes)

print("\nMissing values:")
print(train_df.isnull().sum())


def engineer_features(df):
    """Create new features from the data"""
    df = df.copy()

    # Extract date features
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_year'] = df['date'].dt.dayofyear
    df['week_of_year'] = df['date'].dt.isocalendar().week

    # Fill missing weight with median
    if 'weight' in df.columns:
        df['weight'] = df['weight'].fillna(df['weight'].median())

    # Fill missing market_index with median (if exists)
    if 'market_index' in df.columns:
        df['market_index'] = df['market_index'].fillna(df['market_index'].median())
    else:
        # Add default market_index for december data
        df['market_index'] = 0.95

    # Fill missing quote_signal with median (if exists)
    if 'quote_signal' in df.columns:
        df['quote_signal'] = df['quote_signal'].fillna(df['quote_signal'].median())
    else:
        # Add default quote_signal for december data
        df['quote_signal'] = 2.0

    # Rate per mile (if posted_rate exists)
    if 'posted_rate' in df.columns:
        df['rate_per_mile'] = df['posted_rate'] / df['distance']
        df['rate_per_pound'] = df['posted_rate'] / df['weight']

    # Weight per mile
    df['weight_per_mile'] = df['weight'] / df['distance']

    # Equipment type encoding
    equipment_dummies = pd.get_dummies(df['equipment'], prefix='equipment')
    df = pd.concat([df, equipment_dummies], axis=1)

    # Ensure all equipment columns exist
    for col in ['equipment_Dry Van', 'equipment_Flatbed', 'equipment_Reefer']:
        if col not in df.columns:
            df[col] = 0

    # Note: distance_category and weight_category are engineered but not used in modeling
    # Note: rate_per_mile and rate_per_pound are only available for training data (has posted_rate)
    # These are computed for analysis but not included in feature_cols for the model

    # Location-based features (using pickup/delivery cities)
    # For now, we'll encode them
    return df

print("\nEngineering features...")
train_df = engineer_features(train_df)
validation_df = engineer_features(validation_df)
december_df = engineer_features(december_df)


print("\nSplitting training data...")

# Features to use
feature_cols = [
    'distance', 'weight', 'market_index', 'quote_signal',
    'year', 'month', 'day', 'day_of_week', 'day_of_year', 'week_of_year',
    'weight_per_mile',
    'equipment_Dry Van', 'equipment_Flatbed', 'equipment_Reefer'
]

# For training data, we have posted_rate as target
X = train_df[feature_cols]
y = train_df['posted_rate']

# Fill any remaining NaN values
X = X.fillna(0)

# SPLIT 1: Random 80-20 split (current approach)
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Random split - Training set: {X_train.shape}")
print(f"Random split - Validation set: {X_val.shape}")

# SPLIT 2: Chronological/Time-based split (more realistic for forecasting)
# Sort by date first
train_df_sorted = train_df.sort_values('date')
X_sorted = train_df_sorted[feature_cols].fillna(0)
y_sorted = train_df_sorted['posted_rate']

# Use first 80% for training (chronologically earlier data)
split_idx = int(len(X_sorted) * 0.8)
X_train_chrono = X_sorted.iloc[:split_idx]
y_train_chrono = y_sorted.iloc[:split_idx]
X_val_chrono = X_sorted.iloc[split_idx:]
y_val_chrono = y_sorted.iloc[split_idx:]

print(f"\nChronological split - Training set: {X_train_chrono.shape}")
print(f"Chronological split - Validation set: {X_val_chrono.shape}")
print(f"Chronological split - Training date range: {train_df_sorted.iloc[:split_idx]['date'].min()} to {train_df_sorted.iloc[:split_idx]['date'].max()}")
print(f"Chronological split - Validation date range: {train_df_sorted.iloc[split_idx:]['date'].min()} to {train_df_sorted.iloc[split_idx:]['date'].max()}")


print("\nTraining models...")

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_val_scaled = scaler.transform(X_val)

# Try multiple models
models = {
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
}

best_model = None
best_score = float('inf')
best_model_name = ''

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train_scaled, y_train)

    # Predict on validation set
    y_pred = model.predict(X_val_scaled)

    # Calculate metrics
    mae = mean_absolute_error(y_val, y_pred)
    rmse = np.sqrt(mean_squared_error(y_val, y_pred))
    r2 = r2_score(y_val, y_pred)

    print(f"  MAE: {mae:.2f}")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  R²: {r2:.4f}")

    if mae < best_score:
        best_score = mae
        best_model = model
        best_model_name = name

print(f"\nBest model: {best_model_name} with MAE: {best_score:.2f}")

# Evaluate on chronological split (more realistic for forecasting)
print("\nEvaluating best model on chronological split...")
scaler_chrono = StandardScaler()
X_train_chrono_scaled = scaler_chrono.fit_transform(X_train_chrono)
X_val_chrono_scaled = scaler_chrono.transform(X_val_chrono)

best_model_chrono = type(best_model)(**best_model.get_params())
best_model_chrono.fit(X_train_chrono_scaled, y_train_chrono)
y_pred_chrono = best_model_chrono.predict(X_val_chrono_scaled)

mae_chrono = mean_absolute_error(y_val_chrono, y_pred_chrono)
rmse_chrono = np.sqrt(mean_squared_error(y_val_chrono, y_pred_chrono))
r2_chrono = r2_score(y_val_chrono, y_pred_chrono)

print(f"  Chronological MAE: {mae_chrono:.2f}")
print(f"  Chronological RMSE: {rmse_chrono:.2f}")
print(f"  Chronological R²: {r2_chrono:.4f}")
print(f"  Note: This is a forward-in-time proxy for November/December prediction performance")

print("\nTraining final model on all training data...")
X_all_scaled = scaler.fit_transform(X)
best_model.fit(X_all_scaled, y)


print("\nPredicting on validation data...")

# Prepare validation features
X_validation = validation_df[feature_cols]
X_validation = X_validation.fillna(0)
X_validation_scaled = scaler.transform(X_validation)

# Make predictions
validation_predictions = best_model.predict(X_validation_scaled)

# Create submission dataframe
submission = pd.DataFrame({
    'load_id': validation_df['load_id'],
    'predicted_rate': validation_predictions
})

# Save predictions
submission.to_csv('validation_predictions.csv', index=False)
print("Saved validation_predictions.csv")


print("\nPredicting on December data...")

december_original = pd.read_csv('december-chart-inputs.csv')

# Prepare december features from engineered data
X_december = december_df[feature_cols]
X_december = X_december.fillna(0)
X_december_scaled = scaler.transform(X_december)

# Make predictions
december_predictions = best_model.predict(X_december_scaled)

december_original['predicted_rate'] = december_predictions

# Save december predictions (only original columns + predicted_rate)
december_original.to_csv('december-chart-inputs.csv', index=False)
print("Saved december-chart-inputs.csv with predictions")


print("\nFeature Importance:")
if hasattr(best_model, 'feature_importances_'):
    importance = best_model.feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': feature_cols,
        'importance': importance
    }).sort_values('importance', ascending=False)
    print(feature_importance_df)

print("\nDone!")
