import xgboost as xgb
import shap
import pandas as pd
import numpy as np

class CreditScoringModel:
    def __init__(self):
        # Initialize an XGBoost model
        # For the MVP, we create a model with weights optimized for financial ratios
        self.model = xgb.XGBClassifier(n_estimators=100, max_depth=5, learning_rate=0.1)
        
        # Mock training data following the Five Cs and India context from blueprint
        # Features: [Ratio_ICR, Ratio_DSCR, Ratio_DE, Sentiment_Score, GST_Gap, Bank_Bounce, Litigation_Count]
        X_mock = np.array([
            [4.5, 1.8, 0.4, 0.8, 2, 0, 0], # Good case
            [1.2, 0.9, 2.5, -0.5, 18, 5, 2], # Bad case
            [2.5, 1.2, 1.1, 0.1, 8, 1, 0], # Average
            [5.0, 2.2, 0.2, 0.9, 1, 0, 0], # Excellent
            [0.8, 0.5, 4.0, -0.9, 25, 12, 5] # Very High Risk
        ])
        y_mock = np.array([1, 0, 1, 1, 0]) # 1: Approve, 0: Reject
        
        self.feature_names = ['ICR', 'DSCR', 'DE_Ratio', 'Sentiment', 'GST_Gap', 'Bank_Bounce', 'Litigation']
        self.model.fit(X_mock, y_mock)
        
        # Initialize SHAP explainer
        self.explainer = shap.TreeExplainer(self.model)

    def score(self, features):
        # features should be a dict or list
        if isinstance(features, dict):
            X = pd.DataFrame([features])[self.feature_names]
        else:
            X = pd.DataFrame([features], columns=self.feature_names)
            
        prob = self.model.predict_proba(X)[0][1]
        score = int(prob * 100)
        
        # SHAP calculation
        shap_values = self.explainer.shap_values(X)
        shap_dict = dict(zip(self.feature_names, shap_values[0].tolist()))
        
        # Decision recommendation
        recommendation = "APPROVE" if score >= 70 else ("REFER" if score >= 40 else "REJECT")
        
        # Rationale generation based on SHAP
        positive_factors = sorted([f for f, v in shap_dict.items() if v > 0], key=lambda x: shap_dict[x], reverse=True)[:2]
        negative_factors = sorted([f for f, v in shap_dict.items() if v < 0], key=lambda x: shap_dict[x])[:2]
        
        rationale = f"{recommendation} based on "
        if positive_factors: rationale += f"strong {', '.join(positive_factors)}"
        if negative_factors: rationale += f" despite weaknesses in {', '.join(negative_factors)}"
        
        return {
            "score": score,
            "probability_of_default": 1 - prob,
            "recommendation": recommendation,
            "shap_values": shap_dict,
            "rationale": rationale
        }
