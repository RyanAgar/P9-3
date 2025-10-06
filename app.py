from flask import Flask, request, render_template
from utils.email_parser import parse_email
from rules.scorer import final_score
from ml.feature_extractor import extract_features
from ml.hybrid_scorer import hybrid_score
import joblib

app = Flask(__name__)

# Load ML model and vectorizer once at startup
model, vectorizer = joblib.load("ml/phishing_model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    score = None
    rule_score = None
    ml_score = None
    hybrid_score_result = None

    if request.method == "POST":
        raw_email = request.form["email_content"]
        sender, subject, body, urls = parse_email(raw_email)

        # Rule-based score
        result, rule_score = final_score(sender, subject, body, urls)

        # ML score
        features = extract_features(raw_email)
        X = vectorizer.transform([features])

        # Handle single-class model edge case
        if len(model.classes_) == 1:
            ml_score = model.predict_proba(X)[0][0]
        else:
            phishing_index = list(model.classes_).index("phishing")
            ml_score = model.predict_proba(X)[0][phishing_index]
        
        # Hybrid score (simple average)
        hybrid_score_result = hybrid_score(raw_email)
        score = hybrid_score_result

    # Determine final result based on the hybrid score threshold
    if hybrid_score_result is not None:
        result = "Phishing" if hybrid_score_result >= 5.0 else "Safe"
        
    return render_template(
        "index.html",
        result=result,
        score=score,
        rule_score=round(rule_score, 2) if rule_score is not None else None,
        ml_score=round(ml_score * 10, 2) if ml_score is not None else None,
        hybrid_score=round(hybrid_score_result, 2) if hybrid_score_result is not None else None
    )

if __name__ == "__main__":
    app.run(debug=True)