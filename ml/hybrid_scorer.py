import joblib
from rules.scorer import rule_based_score
from ml.feature_extractor import extract_features
from typing import Dict, Any, Tuple

# Loads trained phishing detection model and its feature 
# Transformer from a saved file so they can be used to analyze new emails 
# and predict phishing risk.
model, vectorizer = joblib.load("ml/phishing_model.pkl")


def hybrid_score(email: str) -> float: # Defines function that takes a raw email string as input.
    features: Dict[str, Any] = extract_features(email) # Extracts structured features from the 
    # email into a dictionary, such as sender_domain, link_count, keyword_score.
    X = vectorizer.transform([features]) # Converts the feature dictionary into 
    # a numeric format using the trained DictVectorizer, preparing it for ML 
    # prediction.
    ml_probability: float = model.predict_proba(X)[0][1] # Uses the trained model
    # to predict the probability that the email is phishing (value 0.0-1.0).
    
    # CRITICAL FIX: Scale the ML probability (0.0-1.0) to the 0.0-10.0 range.
    ml_score_scaled: float = ml_probability * 10.0
    
    rule_score: float = rule_based_score(email) # Computes the rule-based score (0.0-10.0).
    
    # Combines the rule-based score and scaled ML score using weighted average.
    return 0.6 * rule_score + 0.4 * ml_score_scaled