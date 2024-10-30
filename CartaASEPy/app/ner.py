import spacy

custom_ner = spacy.load(r"E:\Licenta\NER_ASE_Model")

def get_entities_from_ner(text):
    doc = custom_ner(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities
