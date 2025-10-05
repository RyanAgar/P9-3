import joblib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#- Ensures Python can import modules from the parent directory (like utils/).
#joblib is used to save and load large Python objects efficiently (like ML models).

from utils.dataset_loader import download_spamassassin, load_dataset
from sklearn.ensemble import RandomForestClassifier
from ml.feature_extractor import extract_features
from sklearn.feature_extraction import DictVectorizer



def train_model():
    path = download_spamassassin()
    emails, labels = load_dataset(path)

    # Feature extraction
    feature_dicts = [extract_features(email) for email in emails]

    # Vectorize features
    vectorizer = DictVectorizer(sparse=False)
    X = vectorizer.fit_transform(feature_dicts)
    y = labels

    # Train model
    model = RandomForestClassifier()
    model.fit(X, y)

    # Save model and vectorizer together
    #- Saves both the trained model and vectorizer as a tuple to phishing_model.pkl
    #This file is later loaded in hybrid_scorer.py for predictions
    joblib.dump((model, vectorizer), "ml/phishing_model.pkl")
    print("Model trained and saved.")


if __name__ == "__main__":
    train_model()