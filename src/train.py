import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from src.data.preprocess import preprocess_data
from src.models.uba_model import create_model

def train_uba_model(data_path, model_save_path, epochs=10, batch_size=32):
    # Load and preprocess the data
    data = pd.read_csv(data_path)
    X, y = preprocess_data(data)

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize the model
    model = create_model()

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)

    # Save the model weights
    model.save_weights(model_save_path)
    print(f"Model weights saved to {model_save_path}")

if __name__ == "__main__":
    train_uba_model(data_path='events/user_events.csv', model_save_path='uba_model_weights.h5', epochs=20, batch_size=64)