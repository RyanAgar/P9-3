import joblib
from utils.dataset_loader import download_spamassassin, load_dataset
from ml.feature_extractor import extract_features

def evaluate_model():
    # Load trained model and vectorizer
    model, vectorizer = joblib.load("ml/phishing_model.pkl")

    # Load dataset
    path = download_spamassassin()
    emails, labels = load_dataset(path)

    # Extract features
    feature_dicts = [extract_features(email) for email in emails]
    X = vectorizer.transform(feature_dicts)

    # Predict
    predictions = model.predict(X)

    # Evaluate
    correct = sum(p == y for p, y in zip(predictions, labels))
    total = len(labels)
    accuracy = correct / total if total > 0 else 0

    print(f"Accuracy: {accuracy:.2f} ({correct}/{total})")

if __name__ == "__main__":
    evaluate_model()
