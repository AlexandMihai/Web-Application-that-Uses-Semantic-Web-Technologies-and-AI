from transformers import pipeline

# Initialize the translation pipelines
translator_en = pipeline("translation_ro_to_en", model="Helsinki-NLP/opus-mt-ro-en")
translator_ro = pipeline("translation_en_to_ro", model="Helsinki-NLP/opus-mt-en-ro")

def paraphrase(sentence):
    translated_to_en = translator_en(sentence)[0]['translation_text']
    paraphrased = translator_ro(translated_to_en)[0]['translation_text']
    return paraphrased

# Example usage
original_sentence = "Care este nivelul de acreditare al ASE?"
paraphrased_sentence = paraphrase(original_sentence)
print("Original:", original_sentence)
print("Paraphrased:", paraphrased_sentence)