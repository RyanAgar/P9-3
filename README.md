# Phish_Guardian
P9-3 INF1002

## Installation
```
pip install -r requirements.txt
```

## Usage
```
# 🔧 Launch the Flask app
python app.py

# 📥 Load and prepare the SpamAssassin dataset
python utils/dataset_loader.py

# 📊 Evaluate the dataset using rule-based and ML scoring
python evaluate_dataset.py

# 🧠 Train the machine learning model (RandomForest + DictVectorizer) (Ensure to run datase)
$env:PYTHONPATH="." (type this before running model_trainer.py)
python ml/model_trainer.py

# 🧪 Hybrid scoring logic (used internally by app.py)
# Combines rule-based and ML predictions for final phishing risk score
# No need to run directly unless testing
python ml/hybrid_scorer.py

```
