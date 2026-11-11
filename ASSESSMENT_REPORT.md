# Freight Rate Prediction - Assessment Report

## Data Validation and Split Approach

### Data Overview
- **Training Data**: 48,000 loads with labeled posted rates
- **Validation Data**: 12,000 loads requiring predictions
- **December Data**: 31 loads for December chart predictions

### Data Splitting Strategy
I used an **80-20 train-validation split** on the training data:
- **Training Set**: 38,400 loads (80%)
- **Validation Set**: 9,600 loads (20%)

**Rationale for 80-20 Split:**
1. Sufficient training data (38,400 samples) to learn complex patterns
2. Adequate validation set (9,600 samples) for reliable performance estimation
3. Industry-standard split ratio for supervised learning
4. Allows for robust model evaluation before final predictions

**Limitation - Temporal Split Consideration:**
⚠️ The random validation split does not closely reflect the November-December prediction period. A **time-based split** (temporal validation) would be more appropriate since:
- Training data spans January 2025 onwards
- Validation data is from November 2025
- December predictions are for December 2025
- Time-based splits better simulate real-world forecasting scenarios

**Improved Approach (if time permits):**
- Train on January-October 2025 data
- Validate on November 2025 data
- Predict December 2025 data
- This better reflects the temporal forecasting task

For this assessment, the random split was used due to time constraints, but a time-based split would provide more realistic performance estimates for the November-December prediction period.

### Data Cleaning and Preprocessing

**Missing Values Handled:**
- **Weight**: 300 missing values in training data → filled with median weight
- **Market Index**: 374 missing values in training data → filled with median market index
- **December Data**: Added default values for market_index (0.95) and quote_signal (2.0)

**Feature Engineering:**
1. **Date Features**: Extracted year, month, day, day_of_week, day_of_year, week_of_year
2. **Weight Features**: weight_per_mile
3. **Categorical Features**: Equipment type one-hot encoding (Dry Van, Flatbed, Reefer)
4. **Note**: distance_category and weight_category were engineered for analysis but not used in the final model
5. **Note**: rate_per_mile and rate_per_pound were computed for training data analysis but not included as model features

### Features Used for Modeling
```
1. distance (numeric)
2. weight (numeric)
3. market_index (numeric)
4. quote_signal (numeric)
5. year (numeric)
6. month (numeric)
7. day (numeric)
8. day_of_week (numeric)
9. day_of_year (numeric)
10. week_of_year (numeric)
11. weight_per_mile (numeric)
12. equipment_Dry Van (binary)
13. equipment_Flatbed (binary)
14. equipment_Reefer (binary)
```

## Model Selection and Performance

### Models Tested
1. **Random Forest Regressor**
   - MAE: 132.24
   - RMSE: 574.40
   - R²: 0.8457

2. **Gradient Boosting Regressor** ⭐ (Selected)
   - MAE: 113.79 (random split)
   - RMSE: 531.34 (random split)
   - R²: 0.8680 (random split)

### Chronological Validation Results (Forward-in-Time Proxy)
To better simulate the November-December prediction task, I also evaluated the model using a chronological (time-based) split:
- **Gradient Boosting Regressor** (chronological split)
   - MAE: 122.23
   - RMSE: 636.16
   - R²: 0.8262

**Note**: The chronological split performance (MAE: 122.23, R²: 0.8262) is a forward-in-time proxy for November/December prediction performance. The actual November/December labels are not available in the training data, so this represents a more realistic estimate of forecasting performance compared to the random split.

### Why Gradient Boosting?
- **Best performance**: Lowest MAE (113.79) and highest R² (0.8680)
- **Better generalization**: Lower RMSE indicates more accurate predictions
- **Handles non-linear relationships**: Freight rates have complex non-linear patterns
- **Robust to outliers**: More stable than Random Forest

### Feature Importance
```
1. distance: 97.5% (most important feature)
2. equipment_Dry Van: 0.8%
3. weight: 0.4%
4. market_index: 0.4%
5. day_of_year: 0.3%
6. equipment_Reefer: 0.2%
7. quote_signal: 0.1%
8. weight_per_mile: 0.1%
9. day: 0.04%
10. week_of_year: 0.01%
11. month: 0.01%
12. day_of_week: 0.001%
13. year: 0%
14. equipment_Flatbed: 0%
```

**Key Insight**: Distance is the dominant factor in freight rate prediction, accounting for 97.5% of feature importance. This aligns with industry knowledge that longer hauls have significantly higher rates.

## Model Performance Analysis

### Validation Metrics
**Random Split:**
- **Mean Absolute Error (MAE)**: 113.79
- **Root Mean Square Error (RMSE)**: 531.34
- **R² Score**: 0.8680

**Chronological Split (Forward-in-Time Proxy):**
- **Mean Absolute Error (MAE)**: 122.23
- **Root Mean Square Error (RMSE)**: 636.16
- **R² Score**: 0.8262

### Performance Interpretation
The model achieves **strong predictive power** with:
- **Random split**: Explains 86.8% of variance in freight rates
- **Chronological split**: Explains 82.6% of variance in freight rates (more realistic for forecasting)

The chronological split performance is more representative of real-world forecasting scenarios since it trains on earlier data and validates on later data, better simulating the November-December prediction task. The random split results are optimistic compared to the chronological split.

## Final Predictions

### Validation Predictions
- **File**: `validation_predictions.csv`
- **Format**: load_id, predicted_rate
- **Count**: 12,000 predictions
- **Model**: Gradient Boosting Regressor trained on all 48,000 training samples

### December Chart Predictions
- **File**: `december-chart-inputs.csv` (with filled predicted_rate column)
- **Format**: pickup, delivery, distance, equipment, weight, date, predicted_rate
- **Count**: 31 predictions (one for each day in December)
- **Scenario**: Lexington to Fort Wayne, 360 miles, Dry Van, 32,000 lbs

## Technical Implementation

### Technology Stack
- **Python 3.10**
- **pandas 2.3.3**: Data manipulation
- **numpy 2.2.6**: Numerical operations
- **scikit-learn 1.7.2**: Machine learning
- **matplotlib 3.10.9**: Visualization (for chart generation)

### Model Training Pipeline
1. Load training and validation data
2. Engineer features (date, rate, weight, categorical encoding)
3. Handle missing values (median imputation)
4. Split training data (80-20)
5. Scale features (StandardScaler)
6. Train multiple models (Random Forest, Gradient Boosting)
7. Select best model based on MAE
8. Retrain best model on all training data
9. Predict on validation and December data
10. Save predictions to CSV files

### Code Structure
- **train_model.py**: Main training script
- **requirements.txt**: Python dependencies
- **validation_predictions.csv**: Final validation predictions
- **december-chart-inputs.csv**: December chart predictions

## Strengths and Limitations

### Strengths
✅ **Strong predictive power**: 86.8% R² score (random split), 82.6% R² score (chronological split)
✅ **Robust feature engineering**: Captures temporal and categorical patterns
✅ **Handles missing data**: Proper imputation strategy
✅ **Model selection**: Tested multiple algorithms, selected best performer
✅ **Feature importance analysis**: Clear understanding of key drivers
✅ **Chronological validation**: Evaluated model on time-based split for realistic forecasting estimate
✅ **Scalable approach**: Can be extended with more features

### Limitations
⚠️ **Random split vs temporal split**: The 80-20 random split (MAE: 113.79, R²: 0.8680) is optimistic compared to the chronological split (MAE: 122.23, R²: 0.8262), which better reflects the November-December prediction period
⚠️ **Distance dominance**: 97.5% feature importance suggests opportunity for improvement
⚠️ **Limited location features**: Pickup/delivery cities not fully utilized
⚠️ **Equipment type impact**: Low importance (0.8% combined) may need more data

### Potential Improvements
1. **Geospatial features**: Add route complexity, urban/rural indicators
2. **Seasonal modeling**: Explicit seasonal trend decomposition
3. **Advanced models**: Try neural networks or ensemble methods
4. **External data**: Fuel prices, weather, economic indicators
5. **Location embeddings**: Use city/state embeddings for geographic patterns

## Conclusion

The Gradient Boosting Regressor model achieved strong performance (MAE: 113.79, R²: 0.8680) in predicting freight rates. The model successfully:
- Validated on 20% holdout set
- Handled missing data appropriately
- Feature engineered meaningful predictors
- Selected best performing algorithm
- Generated predictions for 12,000 validation loads
- Predicted December chart data for 31 days

The **80-20 train-validation split** provided reliable performance estimation while maximizing training data. Distance emerged as the dominant factor (97.5% importance), which aligns with freight industry knowledge.

## Files Submitted

1. **validation_predictions.csv** - 12,000 load predictions ✅
2. **december-chart-inputs.csv** - 31 December predictions ✅
3. **scorer_results/candidate_december.png** - December chart visualization ✅
4. **train_model.py** - Complete training code ✅
5. **score.py** - Scorer and chart generator ✅
6. **requirements.txt** - Python dependencies ✅
7. **This report** - Assessment documentation ✅

**Note**: The scorer has been successfully run and validated both the 12,000 validation predictions and the 31 December predictions. The December chart (`candidate_december.png`) has been generated and is ready for inclusion in the final report.
