# This file is the Maternal Risk Prediction Module.
# It loads patient data, trains an AI model, and predicts health risk levels.

# Import the pandas library and nickname it "pd" so we can use it easily
import pandas as pd

# Import Random Forest - the type of AI model we use to classify risk levels
from sklearn.ensemble import RandomForestClassifier

# Import a tool that checks how many predictions the model got right
from sklearn.metrics import accuracy_score

# Import a tool that splits data into a training part and a testing part
from sklearn.model_selection import train_test_split

# Define a function that reads the CSV file and returns the data as a table
def load_data(filepath="maternal_health_risk.csv"):
    # Open the CSV file and load all rows and columns into a table called "data"
    data = pd.read_csv(filepath)
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


# Define a function that creates and trains the Random Forest model
def train_model(X, y):
    # Create a new Random Forest model (random_state=42 keeps results the same each run)
    model = RandomForestClassifier(random_state=42)
    # Teach the model by showing it all the inputs (X) and correct answers (y)
    model.fit(X, y)
    # Send the trained model back to whoever called this function
    return model


# Define a function that predicts risk for one patient using a trained model
def predict_risk(model, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    # Build a one-row table with this patient's six health measurements
    patient_data = pd.DataFrame(
        # Put all six numbers in one row inside double square brackets
        [[age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate]],
        # Give each number the same column name the model was trained on
        columns=["Age", "SystolicBP", "DiastolicBP", "BS", "BodyTemp", "HeartRate"],
    )
    # Ask the trained model to predict the risk level for this patient
    prediction = model.predict(patient_data)
    # Return the first (and only) prediction as plain text, e.g. "high risk"
    return prediction[0]


# Create an empty "memory box" to store the trained model (None means nothing saved yet)
_trained_model = None

# Create an empty "memory box" to store the model's accuracy score (None means not calculated yet)
_model_accuracy = None


# Define an internal helper function that trains the model once and saves it in memory
def _ensure_model_ready(filepath="maternal_health_risk.csv"):
    # Tell Python we want to use and update the two memory boxes defined above
    global _trained_model, _model_accuracy

    # Only train if we have not already saved a model (avoids retraining every time)
    if _trained_model is None:
        # Load the full dataset from the CSV file
        data = load_data(filepath)
        # Split the data into input columns (X) and answer column (y)
        X, y = prepare_features_and_target(data)
        # Split the data: 80% for training the model, 20% for testing how good it is
        X_train, X_test, y_train, y_test = train_test_split(
            # The inputs and answers to split
            X, y,
            # Use 20% of the data for testing
            test_size=0.2,
            # Fixed random split so we get the same result every time
            random_state=42
        )
        # Train the model using only the 80% training portion
        _trained_model = train_model(X_train, y_train)
        # Ask the trained model to predict risk for the 20% test patients
        predictions = _trained_model.predict(X_test)
        # Calculate accuracy as a percentage and round to one decimal place
        _model_accuracy = round(accuracy_score(y_test, predictions) * 100, 1)

    # Send back both the saved model and its accuracy score
    return _trained_model, _model_accuracy


# Define the main function the Streamlit app calls to get a risk prediction
def predict_maternal_risk(age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate):
    # Make sure the model is trained; get the model back (ignore accuracy with _)
    model, _ = _ensure_model_ready()
    # Use the trained model to predict and return the risk level text
    return predict_risk(
        # Pass the model and all six patient measurements to predict_risk
        model, age, systolic_bp, diastolic_bp, bs, body_temp, heart_rate
    )


# Define a function that returns how accurate the model is on test data
def get_model_accuracy(filepath="maternal_health_risk.csv"):
    # Make sure the model is trained; get the accuracy back (ignore model with _)
    _, accuracy = _ensure_model_ready(filepath)
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
