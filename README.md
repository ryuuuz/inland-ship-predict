# Inland Ship Predict

## Project Overview

The Inland Ship Predict project aims to predict the behavior of inland ships based on various data sources such as ship logs, weather data, and more. The goal is to improve navigation efficiency and safety for inland waterways.

## File Structure

```
inland-ship-predict/
├── data/
│   ├── raw/
│   │   ├── ship_data_2023.csv
│   │   ├── weather_data_2023.csv
│   │   └── ...
│   ├── processed/
│   │   ├── processed_ship_data.csv
│   │   └── processed_weather_data.csv
├── models/
│   ├── model_v1.pkl
│   ├── model_v2.pkl
│   └── ...
├── notebooks/
│   ├── data_exploration.ipynb
│   ├── model_training.ipynb
│   └── model_evaluation.ipynb
├── src/
│   ├── data_processing.py
│   ├── feature_engineering.py
│   ├── model_training.py
│   ├── model_evaluation.py
│   └── utils.py
├── tests/
│   ├── test_data_processing.py
│   ├── test_feature_engineering.py
│   ├── test_model_training.py
│   ├── test_model_evaluation.py
│   └── ...
├── .gitignore
├── README.md
├── requirements.txt
└── setup.py
```

## Data

- **data/raw/**: Contains the raw datasets, including ship data and weather data.
- **data/processed/**: Contains the processed datasets that are ready for model training.

## Models

- **models/**: Contains saved models in `.pkl` format.

## Notebooks

- **notebooks/**: Contains Jupyter notebooks for data exploration, model training, and model evaluation.

## Source Code

- **src/**: Contains the source code for data processing, feature engineering, model training, model evaluation, and utility functions.

## Tests

- **tests/**: Contains unit tests for the various components of the project.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/inland-ship-predict.git
   ```

2. Navigate to the project directory:
   ```bash
   cd inland-ship-predict
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the tests to ensure everything is set up correctly:
   ```bash
   pytest tests/
   ```

## Usage

1. **Data Processing**:
   Run the data processing script to prepare the datasets.
   ```bash
   python src/data_processing.py
   ```

2. **Feature Engineering**:
   Run the feature engineering script to create features for the model.
   ```bash
   python src/feature_engineering.py
   ```

3. **Model Training**:
   Train the model using the training script.
   ```bash
   python src/model_training.py
   ```

4. **Model Evaluation**:
   Evaluate the trained model using the evaluation script.
   ```bash
   python src/model_evaluation.py
   ```
