def find_entity_positions(text, entity_text, entity_label):
    start_pos = text.find(entity_text)
    if start_pos == -1:
        return None
    end_pos = start_pos + len(entity_text)
    return (start_pos, end_pos, entity_label)

def prepare_ner_data(sentences, entity_texts, entity_label):
    data = []
    for sentence, entity_text in zip(sentences, entity_texts):
        entity_positions = find_entity_positions(sentence, entity_text, entity_label)
        if entity_positions:
            data.append((sentence, {"entities": [entity_positions]}))
        else:
            print(f"Warning: '{entity_text}' not found in '{sentence}'")
    return data

sentences = [
    # Complete sentences with diacritics
    "Ce întrebări frecvente primesc studenții noi?",
    "Ce tipuri de întrebări sunt adresate în sesiunile de orientare?",
    "Ce întrebări pot adresa candidații interesați de ASE?",
    "Ce întrebări sunt esențiale pentru înțelegerea programului?",
    "Ce întrebări comune au studenții despre regulamente?",

    # Simpler sentences without diacritics
    "Intrebari frecvente",
    "Intrebari des puse",
    "Intrebari uzuale",
    "Intrebari de la studenti",
    "Intrebari in sesiuni",
    "Intrebari obisnuite",
    "Tipuri de intrebari",
    "Intrebari comune",
    "Intrebari curente",
    "Intrebari tipice",

    # Even simpler keywords or short phrases
    "Intrebari studenti",
    "FAQ studenti",
    "Intrebari ASE",
    "Intrebari orientare",
    "Intrebari frecvente",
    "FAQ ASE",
    "Intrebari reguli",
    "Intrebari generale",
    "Intrebari sesiuni",
    "Intrebari admitere"
]

entity_texts = [
    "întrebări frecvente",
    "tipuri de întrebări",
    "întrebări",
    "întrebări esențiale",
    "întrebări comune",

    "Intrebari frecvente",
    "Intrebari des puse",
    "Intrebari uzuale",
    "Intrebari de la studenti",
    "Intrebari in sesiuni",
    "Intrebari obisnuite",
    "Tipuri de intrebari",
    "Intrebari comune",
    "Intrebari curente",
    "Intrebari tipice",

    "Intrebari studenti",
    "FAQ studenti",
    "Intrebari ASE",
    "Intrebari orientare",
    "Intrebari frecvente",
    "FAQ ASE",
    "Intrebari reguli",
    "Intrebari generale",
    "Intrebari sesiuni",
    "Intrebari admitere"
]

entity_label = "INTREBARI"

ner_data = prepare_ner_data(sentences, entity_texts, entity_label)

for item in ner_data:
    print(str(item) + ",")