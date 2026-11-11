# Freight Rate Prediction Challenge

Machine learning model to predict freight rates for trucking loads.

## Overview

This project implements a Gradient Boosting Regressor to predict freight rates based on load characteristics including distance, weight, equipment type, and temporal features.

## Model Performance

- **MAE**: 113.79
- **RMSE**: 531.34
- **R²**: 0.8680

## Features

- Distance (97.5% importance)
- Equipment type (Dry Van, Flatbed, Reefer)
- Weight
- Market index
- Quote signal
- Temporal features (day of week, day of year, week of year)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Train the model and generate predictions:

```bash
python train_model.py
```

This will:
1. Load training data from `train-test.csv`
2. Engineer features and handle missing values
3. Train Gradient Boosting Regressor
4. Generate predictions for `validation.csv`
5. Save results to `validation_predictions.csv`
6. Predict December chart data in `december-chart-inputs.csv`

### Run the scorer:

```bash
python score.py --predictions validation_predictions.csv --december-predictions december-chart-inputs.csv
```

This will:
- Validate the 12,000 validation predictions
- Validate the 31 December predictions
- Generate `scorer_results/candidate_december.png` chart

### Or run everything at once:

```bash
python run_all.py
```

## Data

- **train-test.csv**: 48,000 labeled loads for training
- **validation.csv**: 12,000 loads requiring predictions
- **december-chart-inputs.csv**: 31 loads for December chart
- **validation-predictions-template.csv**: Template for validation predictions

## Project Structure

```
.
├── train-test.csv                          # Training data
├── validation.csv                         # Validation data
├── december-chart-inputs.csv              # December chart data
├── validation-predictions-template.csv    # Prediction template
├── validation_predictions.csv             # Generated predictions
├── train_model.py                         # Training script
├── requirements.txt                       # Dependencies
└── ASSESSMENT_REPORT.md                   # Detailed report
```

## Methodology

### Data Split
- 80% training (38,400 samples)
- 20% validation (9,600 samples)

### Feature Engineering
- Date features (year, month, day, day_of_week, day_of_year, week_of_year)
- Rate features (rate_per_mile, rate_per_pound)
- Weight features (weight_per_mile)
- Equipment type one-hot encoding
- Distance and weight categories

### Models Tested
1. Random Forest Regressor (MAE: 132.24, R²: 0.8457)
2. Gradient Boosting Regressor (MAE: 113.79, R²: 0.8680) ✅ Selected

### Data Cleaning
- Missing weight values filled with median
- Missing market_index values filled with median
- December data: default values for market_index and quote_signal

## Output Files

- `validation_predictions.csv`: 12,000 load predictions
- `december-chart-inputs.csv`: 31 December predictions with predicted_rate column

## Assessment Report

See `ASSESSMENT_REPORT.md` for detailed methodology, performance analysis, and feature importance.

## Requirements

- Python 3.10+
- pandas >= 2.0
- numpy >= 1.26
- scikit-learn >= 1.3
- matplotlib >= 3.8
