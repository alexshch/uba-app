import pandas as pd
from sklearn.preprocessing import StandardScaler

def clean_data(df):
    df = df.dropna()  # Remove missing values
    df = df.drop_duplicates()  # Remove duplicate entries
    return df

def normalize_features(df):
    scaler = StandardScaler()
    numerical_features = df.select_dtypes(include=['float64', 'int64']).columns
    df[numerical_features] = scaler.fit_transform(df[numerical_features])
    return df

def preprocess_data(file_path):
    df = pd.read_csv(file_path)  # Load the dataset
    df = clean_data(df)  # Clean the data
    df = normalize_features(df)  # Normalize features
    return df

def prepare_dataset(file_path):
    df = preprocess_data(file_path)
    # Additional preprocessing steps can be added here
    return df