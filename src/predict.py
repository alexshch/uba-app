import numpy as np
import tensorflow as tf
from src.models.uba_model import create_model  # Assuming a function to create the model is defined here
from src.data.preprocess import preprocess_data  # Function to preprocess new user event data

def load_model(model_path):
    model = create_model()
    model.load_weights(model_path)
    return model

def predict_user_action(model, user_events):
    processed_events = preprocess_data(user_events)
    predictions = model.predict(processed_events)
    return predictions

if __name__ == "__main__":
    model_path = "path/to/your/model_weights.h5"  # Update with the actual path
    model = load_model(model_path)

    # Example user events input
    user_events = [
        # Add user event data here
    ]

    predictions = predict_user_action(model, user_events)
    print("Predictions:", predictions)