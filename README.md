# Fake Job Postings Analysis Project

This project analyzes and processes job posting data to identify potentially fraudulent listings. It includes various components for data cleaning, feature engineering, and model training.

## Project Structure

### Data Cleaning Scripts
- `clean_description.py` & `clean_description2.py` - Clean job descriptions
- `clean_requirements.py` & `clean_requirements_improve.py` - Clean job requirements
- `clean_title.py` - Clean job titles
- `clean_wage_data.py` - Clean salary information
- `company_profile.py` - Clean company profiles
- `location_splitting.py` - Process location data

### Feature Engineering
- `feature_description.py` - Extract features from descriptions
- `feature_engineer_title.py` - Extract features from titles
- `feature_engineer_requirements.py` - Extract features from requirements
- `feature_company_profile.py` - Extract features from company profiles
- `mapping_exp_edu.py` - Map experience and education levels
- `onehot_encode_categories.py` - One-hot encode categorical variables

### Analysis and Testing
- `analyze_jobs.py` - General job data analysis
- `missing_values.py` - Analyze missing values
- `test_description.py` - Test description cleaning
- `test_clean_requirements.py` - Test requirements cleaning
- `inspect_feature_importances.py` - Analyze feature importance

### Model Training
- `train_lightgbm.py` - Train LightGBM model
- `sampling.py` - Handle data sampling
- `merge_data.py` - Merge processed data

### API Service
- `fast_api_service.py` - FastAPI service for model deployment

## Data Files
- `fake_job_postings.csv` - Raw job posting data
- Various cleaned and processed data files:
  - `cleaned_description.xlsx`
  - `cleaned_requirements.csv`
  - `cleaned_title_benefits.csv`
  - `cleaned_company_profile.xlsx`
  - And more...

## Model Files
- `model.pkl` - Trained model
- `feature_columns.pkl` - Feature column information

## Setup and Installation

1. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

2. Data Processing Pipeline:
   - Start with raw data in `fake_job_postings.csv`
   - Run cleaning scripts for each component (description, requirements, etc.)
   - Run feature engineering scripts
   - Merge processed data
   - Train model

## Usage

### Data Cleaning
```bash
python clean_description.py
python clean_requirements.py
python clean_title.py
python company_profile.py
```

### Feature Engineering
```bash
python feature_description.py
python feature_engineer_title.py
python feature_engineer_requirements.py
```

### Model Training
```bash
python train_lightgbm.py
```

### API Service
```bash
python fast_api_service.py
```

## Requirements
- Python 3.8+
- pandas
- openpyxl
- scikit-learn
- lightgbm
- fastapi
- And other dependencies listed in requirements.txt 