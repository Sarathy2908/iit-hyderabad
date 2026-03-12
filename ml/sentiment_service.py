from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import jobres
import os

class SentimentClassifier:
    def __init__(self):
        # In a real scenario, we would load a pre-trained model
        # For the hackathon MVP, we use a simple rule-based approach or 
        # initialize a basic TF-IDF + LR with some mock intelligence
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.model = LogisticRegression()
        
        # Mock training for common financial keywords
        train_texts = [
            "profit surged beating estimates", "revenue growth above targets",
            "stock downgrade due to loss", "factory closure and strike",
            "regulatory notice for compliance failure", "court case filed for fraud",
            "stable performance for the quarter", "meeting held for new expansion"
        ]
        train_labels = ["POSITIVE", "POSITIVE", "NEGATIVE", "NEGATIVE", "REGULATORY_RISK", "LITIGATION", "NEUTRAL", "NEUTRAL"]
        
        X = self.vectorizer.fit_transform(train_texts)
        self.model.fit(X, train_labels)

    def predict(self, text):
        X = self.vectorizer.transform([text])
        label = self.model.predict(X)[0]
        proba = max(self.model.predict_proba(X)[0])
        return label, float(proba)

    def analyze_batch(self, headlines):
        results = []
        for h in headlines:
            label, score = self.predict(h)
            results.append({"headline": h, "label": label, "confidence": score})
        return results
