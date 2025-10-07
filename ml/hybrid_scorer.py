import joblib
from rules.scorer import rule_based_score
from ml.feature_extractor import extract_features
from typing import Dict, Any, Tuple

# Loads trained phishing detection model and its feature
# Transformer from a saved file so they can be used to analyze new emails
# And predict phishing risk.
model, vectorizer = joblib.load("ml/phishing_model.pkl")


def hybrid_score(email: str) -> float: # Defines function that takes a raw email string as input.
    features: Dict[str, Any] = extract_features(email) # Extracts structured features from the
    # email into a dictionary, such as sender_domain, link_count, keyword_score
    # With function imported from feature_extractor.py
    X = vectorizer.transform([features]) # Converts the feature dictionary into
    # a numeric format using the trained DictVectorizer, preparing it for ML
    # prediction.
    ml_probability: float = model.predict_proba(X)[0][1] # Uses the trained RandomForestClassifier
    # to predict the probability that the email is phishing. [0][1] accesses the
    # probability for the "phishing" class.
    
    #Scale the ML probability (0.0-1.0) to the 0.0-10.0 range.
    ml_score_scaled: float = ml_probability * 10.0
    
    rule_score: float = rule_based_score(email) # Computes a rule-based score using
    # handcrafted logic (e.g., domain spoofing, suspicious URLs, keyword density).
    # returns a value between 0 and 10 (fixed scale).
    
    # Combines the rule-based score and scaled ML score using weighted average,
    # with more weight given to the rule-based score (60% vs. 40%).
    return 0.6 * rule_score + 0.4 * ml_score_scaled