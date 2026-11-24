
import os
import joblib

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


# Step 1: Define model storage location

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_DIR = os.path.join(BASE_DIR, "model")

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "iris_model.joblib"
)


def train_model():

    print("\nStarting Iris ML Model Training...")

    # Step 2: Load Iris dataset

    iris = load_iris()

    X = iris.data
    y = iris.target

    print("\nDataset loaded successfully")

    print("Total samples:", len(X))
    print("Total features:", X.shape[1])
    print("Target classes:", iris.target_names)

    # Step 3: Split dataset into training and testing sets

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    print("\nDataset split completed")

    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))

    # Step 4: Create ML pipeline

    model_pipeline = Pipeline([
        (
            "scaler",
            StandardScaler()
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=200,
                random_state=42
            )
        )
    ])

    # Step 5: Train the model

    model_pipeline.fit(
        X_train,
        y_train
    )

    print("\nModel training completed")

    # Step 6: Generate predictions

    y_pred = model_pipeline.predict(X_test)

    # Step 7: Evaluate model performance

    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    print("\nModel Evaluation Results")

    print("------------------------------")

    print(f"Accuracy: {accuracy:.4f}")

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            y_pred,
            target_names=iris.target_names
        )
    )

    print("\nConfusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    # Step 8: Save the trained model

    os.makedirs(
        MODEL_DIR,
        exist_ok=True
    )

    joblib.dump(
        model_pipeline,
        MODEL_PATH
    )

    print("\nModel saved successfully")

    print("Model location:", MODEL_PATH)

    print("\nTraining process completed!")


if __name__ == "__main__":
    train_model()
