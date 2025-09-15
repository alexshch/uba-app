# User Behavior Analytics (UBA) Project

## Overview

The User Behavior Analytics (UBA) project aims to develop a neural network-based system that analyzes user behavior to determine if subsequent actions belong to the same user or a different one. The model is trained on various user events, including authentication times, IP addresses, terminal commands, and service/process names.

## Project Structure

```
uba-app
├── src
│   ├── data
│   │   └── preprocess.py       # Data preprocessing functions
│   ├── models
│   │   └── uba_model.py         # UBA model definition
│   ├── train.py                 # Model training script
│   ├── predict.py               # Prediction script
│   └── utils
│       └── feature_extraction.py # Feature extraction utilities
├── requirements.txt             # Project dependencies
├── README.md                    # Project documentation
└── config.yaml                  # Configuration settings
```

## Presetup instruction (you need python 3.10)

1. Install required dependencies:

   ```
   sudo apt update
   sudo apt install -y software-properties-common
   ```

2. Add deadsnakes repository:

   ```
   sudo add-apt-repository ppa:deadsnakes/ppa
   sudo apt update
   ```

3. Install Python 3.10:
   ```
   sudo apt install -y python3.10 python3.10-venv python3.10-dev
   ```
4. Check installation:
   ```
   python3.10 --version
   ```
   5

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd uba-app
   ```
2. Create virtual environment:

   ```
   python3.10 -m venv .venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Configure the `config.yaml` file with appropriate settings for your environment, including model parameters and file paths.

## Usage

1. **Preprocessing Data**: Use the `src/data/preprocess.py` to clean and prepare your user event data for training.

2. **Training the Model**: Run the training script to train the UBA model:

   ```
   python src/train.py
   ```

3. **Making Predictions**: After training, use the prediction script to evaluate new user events:
   ```
   python src/predict.py
   ```

## Example

- To preprocess data, you can call the functions defined in `preprocess.py` to load and clean your dataset.
- The trained model can be evaluated with new user events to check for anomalies or confirm user identity.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
