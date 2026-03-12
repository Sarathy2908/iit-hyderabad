import spacy
from spacy.language import Language

@Language.component("financial_entity_recognizer")
def financial_entity_recognizer(doc):
    # Simple rule-based/regex logic for the MVP
    # In a full version, this would be a trained transformer model
    return doc

def get_financial_ner_pipeline():
    try:
        nlp = spacy.load("en_core_web_sm")
    except:
        # Fallback if model not downloaded
        nlp = spacy.blank("en")
    
    # Add custom patterns for INR amounts, GSTIN, PAN, etc.
    ruler = nlp.add_pipe("entity_ruler", before="ner")
    patterns = [
        {"label": "AMOUNT_INR", "pattern": [{"TEXT": {"REGEX": "^₹?\d+(,\d+)*(\.\d+)?$"}}]},
        {"label": "GSTIN", "pattern": [{"TEXT": {"REGEX": "^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$"}}]},
        {"label": "PAN", "pattern": [{"TEXT": {"REGEX": "^[A-Z]{5}[0-9]{4}[A-Z]{1}$"}}]},
        {"label": "CIN", "pattern": [{"TEXT": {"REGEX": "^[LU][0-9]{5}[A-Z]{2}[0-9]{4}[A-Z]{3}[0-9]{6}$"}}]}
    ]
    ruler.add_patterns(patterns)
    return nlp

class FinancialNER:
    def __init__(self):
        self.nlp = get_financial_ner_pipeline()

    def extract(self, text):
        doc = self.nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })
        return entities
