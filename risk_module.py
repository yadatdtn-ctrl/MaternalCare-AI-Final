# This file is the Maternal Risk Prediction Module.
# It loads patient data, trains an AI model, and predicts health risk levels.

# Import the pandas library and nickname it "pd" so we can use it easily
import pandas as pd

# Import K-Nearest Neighbors (KNN) - the type of AI model we use to classify risk levels
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

# Import a tool that checks how many predictions the model got right
from sklearn.metrics import accuracy_score

# Import a tool that splits data into a training part and a testing part
from sklearn.model_selection import train_test_split

# Define a function that reads the CSV file and returns the data as a table
def load_data(filepath="maternal_health_risk.csv"):
    # Open the CSV file and load all rows and columns into a table called "data"
    data = pd.read_csv(filepath)
    # Remove duplicate rows to match the cleaned dataset
    # used in the team's research notebook.
    data = data.drop_duplicates()
    # Send the table back to whoever called this function
    return data


# Define a function that separates the input columns from the answer column
def prepare_features_and_target(data):
    # List the six health measurement column names we want the model to learn from
    feature_columns = ["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"]
    # Pull only those six columns out of the full table and store them in X (the inputs)
    X = data[feature_columns]
    # Pull the RiskLevel column (the correct answers) and store it in y (the target)
    y = data["RiskLevel"]
    # Send both X and y back to whoever called this function
    return X, y


# Define a function that creates and trains the K-Nearest Neighbors (KNN) model
def train_model(X, y):
    # K-Nearest Neighbors with K=2 - chosen to match the team's
    # finalized research notebook (68.13% accuracy, best of 6 models tested).
    # KNN is distance-based, so we scale features first - this matches
    # the team's notebook which trained on X_train_scaled.
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = KNeighborsClassifier(n_neighbors=2)
    model.fit(X_scaled, y)
    return model, scaler


# Define a function that predicts risk for one patient using a trained model and scaler
def predict_risk(model, scaler, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    # Build a one-row table with this patient's six health measurements
    patient_data = pd.DataFrame(
        # Put all six numbers in one row inside double square brackets
        [[age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate]],
        # Give each number the same column name the model was trained on
        columns=["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"],
    )
    # Scale the patient data using the same scaler fitted during training
    patient_data_scaled = scaler.transform(patient_data)
    # Ask the trained model to predict the risk level for this patient
    prediction = model.predict(patient_data_scaled)
    # Return the first (and only) prediction as plain text, e.g. "high risk"
    return prediction[0]


# Create an empty "memory box" to store the trained model (None means nothing saved yet)
_trained_model = None

# Create an empty "memory box" to store the fitted scaler (None means nothing saved yet)
_scaler = None

# Create an empty "memory box" to store the model's accuracy score (None means not calculated yet)
_model_accuracy = None


# Define an internal helper function that trains the model once and saves it in memory
def _ensure_model_ready(filepath="maternal_health_risk.csv"):
    # Tell Python we want to use and update the three memory boxes defined above
    global _trained_model, _scaler, _model_accuracy

    # Only train if we have not already saved a model (avoids retraining every time)
    if _trained_model is None:
        # Load the full dataset from the CSV file
        data = load_data(filepath)
        # Split the data into input columns (X) and answer column (y)
        X, y = prepare_features_and_target(data)
        # Split the data: 80% for training, 20% for testing.
        # stratify=y matches the team's notebook split - keeps low/mid/high
        # risk proportions balanced across both sets.
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )
        # Train the K-Nearest Neighbors (KNN) model using the 80% training portion
        # train_model returns both the fitted model and the fitted scaler
        _trained_model, _scaler = train_model(X_train, y_train)
        # Scale the test set using the same scaler fitted on training data
        X_test_scaled = _scaler.transform(X_test)
        # Ask the trained model to predict risk for the 20% test patients
        predictions = _trained_model.predict(X_test_scaled)
        # Calculate accuracy as a percentage and round to one decimal place
        _model_accuracy = round(accuracy_score(y_test, predictions) * 100, 1)

    # Send back the saved model, scaler, and accuracy score
    return _trained_model, _scaler, _model_accuracy


# Define the main function the Streamlit app calls to get a risk prediction
def predict_maternal_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    # Make sure the model is trained; get the model and scaler back (ignore accuracy with _)
    model, scaler, _ = _ensure_model_ready()
    # Use the trained model and scaler to predict and return the risk level text
    return predict_risk(
        # Pass the model, scaler, and all six patient measurements to predict_risk
        model, scaler, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate
    )


# Define a function that returns how accurate the model is on test data
def get_model_accuracy(filepath="maternal_health_risk.csv"):
    # Make sure the model is trained; get the accuracy back (ignore model and scaler with _)
    _, _s, accuracy = _ensure_model_ready(filepath)
    # Send the accuracy percentage back to whoever called this function
    return accuracy


# This block only runs when you execute this file directly (python risk_module.py)
if __name__ == "__main__":
    # Predict risk for a sample patient to test that everything works
    risk = predict_maternal_risk(
        # Sample patient values: age 25, blood pressure 130/80, blood sugar 15, etc.
        age=25, systolic_bp=130, diastolic_bp=80, bs=15, body_temp=98, heart_rate=86
    )
    # Print the predicted risk level to the terminal
    print(f"Predicted risk level: {risk}")
    # Print the model's accuracy percentage to the terminal
    print(f"Model accuracy: {get_model_accuracy()}%")
