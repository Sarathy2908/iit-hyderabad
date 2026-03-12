from flask import Flask, request, jsonify
import os
from ner_service import FinancialNER
from sentiment_service import SentimentClassifier
from scoring_service import CreditScoringModel

app = Flask(__name__)

# Initialize services
ner_service = FinancialNER()
sentiment_service = SentimentClassifier()
scoring_service = CreditScoringModel()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/ner', methods=['POST'])
def extract_entities():
    data = request.json
    text = data.get('text', '')
    entities = ner_service.extract(text)
    return jsonify({"entities": entities}), 200

@app.route('/sentiment', methods=['POST'])
def analyze_sentiment():
    data = request.json
    headlines = data.get('headlines', [])
    results = sentiment_service.analyze_batch(headlines)
    return jsonify({"results": results}), 200

@app.route('/score', methods=['POST'])
def compute_score():
    data = request.json
    features = data.get('features', {})
    result = scoring_service.score(features)
    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
