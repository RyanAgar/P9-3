import joblib
from rules.scorer import rule_based_score
from ml.feature_extractor import extract_features


#Loads trained phishing detection model and its feature 
#Transformer from a saved file so they can be used to analyze new emails 
#And predict phishing risk.
model, vectorizer = joblib.load("ml/phishing_model.pkl")


def hybrid_score(email): #Defines function that takes a raw email string as input.
    features = extract_features(email) #Extracts structured features from the 
    #email into a dictionary, such as sender_domain, link_count, keyword_score 
    #with function imported from feature_extractor.py
    X = vectorizer.transform([features]) #Converts the feature dictionary into 
    #a numeric format using the trained DictVectorizer, preparing it for ML 
    #prediction.
    ml_score = model.predict_proba(X)[0][1] #Uses the trained RandomForestClassifier
    #to predict the probability that the email is phishing.[0][1] accesses the 
    #probability for the "phishing" class.
    rule_score = rule_based_score(email) #Computes a rule-based score using 
    #handcrafted logic (e.g., domain spoofing, suspicious URLs, keyword density).
    #returns a value between 0 and 1.
    return 0.6 * rule_score + 0.4 * ml_score
    #Combines the rule-based score and ML score using weighted average,
    #with more weight given to the rule-based score (60% vs. 40%).  