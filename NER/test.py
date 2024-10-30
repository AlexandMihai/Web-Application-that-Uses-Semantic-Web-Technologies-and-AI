import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding
from spacy.scorer import Scorer
import random
import json
from rowordnet import RoWordNet

# Initialize RoWordNet
wn = RoWordNet()

# Initialize spaCy model
nlp = spacy.blank("ro")
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

# Example training data
TRAIN_DATA = [
    ('Care este nivelul de acreditare al ASE?', {'entities': [(10, 31, 'NIVEL_ACREDITARE')]}),
    ('Ce grad de acreditare are Academia de Studii Economice?', {'entities': [(3, 21, 'NIVEL_ACREDITARE')]}),
    ('ASE este clasificată la ce nivel în sistemul de învățământ superior?',
     {'entities': [(27, 32, 'NIVEL_ACREDITARE')]}),
    ('Ce statut de acreditare deține ASE în context academic?', {'entities': [(3, 23, 'NIVEL_ACREDITARE')]}),
    ('La ce standard de acreditare răspunde ASE?', {'entities': [(6, 28, 'NIVEL_ACREDITARE')]}),
    ('Care este clasificarea acreditării pentru ASE în domeniul economic?',
     {'entities': [(10, 34, 'NIVEL_ACREDITARE')]}),
    ('Cum este recunoscută ASE la nivel național și internațional în termeni de acreditare?',
     {'entities': [(28, 59, 'NIVEL_ACREDITARE')]}),
    ('nivel acreditare ASE', {'entities': [(0, 16, 'NIVEL_ACREDITARE')]}),
    ('acreditare ASE nivel', {'entities': [(0, 20, 'NIVEL_ACREDITARE')]}),
    ('ASE grad acreditare', {'entities': [(4, 19, 'NIVEL_ACREDITARE')]}),
    ('statut acreditare ASE', {'entities': [(0, 17, 'NIVEL_ACREDITARE')]}),
    ('clasificare acreditare ASE', {'entities': [(0, 22, 'NIVEL_ACREDITARE')]}),
    ('ASE recunoastere nivel', {'entities': [(4, 22, 'NIVEL_ACREDITARE')]}),
    ('standard acreditare ASE', {'entities': [(0, 19, 'NIVEL_ACREDITARE')]}),
    ('acreditare', {'entities': [(0, 10, 'NIVEL_ACREDITARE')]}),
    ('nivel acreditare', {'entities': [(0, 16, 'NIVEL_ACREDITARE')]}),
    ('grad acreditare', {'entities': [(0, 15, 'NIVEL_ACREDITARE')]}),
    ('recunoastere ASE', {'entities': [(0, 12, 'NIVEL_ACREDITARE')]}),
    ('clasificare ASE', {'entities': [(0, 11, 'NIVEL_ACREDITARE')]}),
    ('ASE acreditata', {'entities': [(4, 14, 'NIVEL_ACREDITARE')]}),
    ('acreditare universitara', {'entities': [(0, 23, 'NIVEL_ACREDITARE')]}),
    ('ASE standard', {'entities': [(4, 12, 'NIVEL_ACREDITARE')]}),
    ('calitate ASE', {'entities': [(0, 8, 'NIVEL_ACREDITARE')]}),
    ('ASE excelenta', {'entities': [(4, 13, 'NIVEL_ACREDITARE')]}),
    ('acreditare superioara ASE', {'entities': [(0, 21, 'NIVEL_ACREDITARE')]}),
    ('ASE recunoastere', {'entities': [(4, 16, 'NIVEL_ACREDITARE')]}),
    ('statut ASE', {'entities': [(0, 6, 'NIVEL_ACREDITARE')]}),
    ('nivel recunoastere', {'entities': [(0, 18, 'NIVEL_ACREDITARE')]}),
    ('ASE calificativ', {'entities': [(4, 15, 'NIVEL_ACREDITARE')]}),

    ('Care este caracterul distinctiv al ASE?', {'entities': [(10, 31, 'CARACTER_UNIVERSITATE')]}),
    ('Ce trăsături definitorii are ASE ca universitate?', {'entities': [(3, 24, 'CARACTER_UNIVERSITATE')]}),
    ('Cum se distinge ASE în peisajul universitar?', {'entities': [(4, 15, 'CARACTER_UNIVERSITATE')]}),
    ('Ce particularități are ASE ca instituție academică?', {'entities': [(3, 18, 'CARACTER_UNIVERSITATE')]}),
    ('ASE este recunoscută pentru ce valori academice?', {'entities': [(31, 47, 'CARACTER_UNIVERSITATE')]}),
    ('caracter ASE', {'entities': [(0, 8, 'CARACTER_UNIVERSITATE')]}),
    ('definire ASE universitate', {'entities': [(0, 8, 'CARACTER_UNIVERSITATE')]}),
    ('distinctie ASE universitar', {'entities': [(0, 10, 'CARACTER_UNIVERSITATE')]}),
    ('particularitati ASE academice', {'entities': [(0, 15, 'CARACTER_UNIVERSITATE')]}),
    ('valori ASE academice', {'entities': [(0, 6, 'CARACTER_UNIVERSITATE')]}),
    ('caracter', {'entities': [(0, 8, 'CARACTER_UNIVERSITATE')]}),
    ('distinctie', {'entities': [(0, 10, 'CARACTER_UNIVERSITATE')]}),
    ('valori academice', {'entities': [(0, 6, 'CARACTER_UNIVERSITATE')]}),
    ('particularitati', {'entities': [(0, 15, 'CARACTER_UNIVERSITATE')]}),
    ('ASE universitate', {'entities': [(4, 16, 'CARACTER_UNIVERSITATE')]}),
    ('Ce face ASE unică academic?', {'entities': [(12, 17, 'CARACTER_UNIVERSITATE')]}),
    ('Identitatea ASE în educație?', {'entities': [(0, 11, 'CARACTER_UNIVERSITATE')]}),
    ('Principii ASE', {'entities': [(0, 9, 'CARACTER_UNIVERSITATE')]}),
    ('Orientări ASE în educație', {'entities': [(0, 9, 'CARACTER_UNIVERSITATE')]}),
    ('Inovație ASE', {'entities': [(0, 8, 'CARACTER_UNIVERSITATE')]}),
    ('ASE și tradițiile academice', {'entities': [(7, 27, 'CARACTER_UNIVERSITATE')]}),
    ('Cultura academică ASE', {'entities': [(0, 17, 'CARACTER_UNIVERSITATE')]}),
    ('ASE și excelența în educație', {'entities': [(7, 28, 'CARACTER_UNIVERSITATE')]}),
    ('Misiunea academică a ASE', {'entities': [(0, 18, 'CARACTER_UNIVERSITATE')]}),
    ('Viziunea ASE în învățământul superior', {'entities': [(0, 8, 'CARACTER_UNIVERSITATE')]}),
    ('Strategia ASE pentru educație', {'entities': [(0, 9, 'CARACTER_UNIVERSITATE')]}),
    ('Abordarea ASE în învățământ', {'entities': [(0, 9, 'CARACTER_UNIVERSITATE')]}),
    ('Contribuția ASE la educație', {'entities': [(0, 11, 'CARACTER_UNIVERSITATE')]}),
    ('ASE ca lider academic', {'entities': [(7, 21, 'CARACTER_UNIVERSITATE')]}),
    ('Rolul ASE în comunitatea academică', {'entities': [(0, 5, 'CARACTER_UNIVERSITATE')]}),

    ('Cum se numește oficial ASE?', {'entities': [(4, 22, 'DENUMIRE_OFICIALA')]}),
    ('Denumirea completă a ASE?', {'entities': [(0, 18, 'DENUMIRE_OFICIALA')]}),
    ('Cum este denumită ASE în actele oficiale?', {'entities': [(4, 17, 'DENUMIRE_OFICIALA')]}),
    ('Titulatura oficială a ASE este?', {'entities': [(0, 19, 'DENUMIRE_OFICIALA')]}),
    ('nume oficial ASE', {'entities': [(0, 12, 'DENUMIRE_OFICIALA')]}),
    ('denumire ASE', {'entities': [(0, 8, 'DENUMIRE_OFICIALA')]}),
    ('titulatura ASE', {'entities': [(0, 10, 'DENUMIRE_OFICIALA')]}),
    ('ASE denumire oficiala', {'entities': [(4, 21, 'DENUMIRE_OFICIALA')]}),
    ('nume ASE', {'entities': [(0, 4, 'DENUMIRE_OFICIALA')]}),
    ('ASE oficial', {'entities': [(4, 11, 'DENUMIRE_OFICIALA')]}),
    ('denumire', {'entities': [(0, 8, 'DENUMIRE_OFICIALA')]}),
    ('titulatura', {'entities': [(0, 10, 'DENUMIRE_OFICIALA')]}),
    ('ASE nume complet', {'entities': [(4, 16, 'DENUMIRE_OFICIALA')]}),
    ('identitate ASE', {'entities': [(0, 10, 'DENUMIRE_OFICIALA')]}),
    ('ASE denumit oficial', {'entities': [(4, 19, 'DENUMIRE_OFICIALA')]}),
    ('ASE sub ce nume opera', {'entities': [(4, 21, 'DENUMIRE_OFICIALA')]}),
    ('nume formal ASE', {'entities': [(0, 11, 'DENUMIRE_OFICIALA')]}),
    ('ASE recunoscut ca', {'entities': [(4, 17, 'DENUMIRE_OFICIALA')]}),
    ('ASE identificat oficial', {'entities': [(4, 23, 'DENUMIRE_OFICIALA')]}),
    ('denumire completa ASE', {'entities': [(0, 17, 'DENUMIRE_OFICIALA')]}),
    ('ASE si numele sau oficial', {'entities': [(4, 25, 'DENUMIRE_OFICIALA')]}),
    ('ASE in documente', {'entities': [(4, 16, 'DENUMIRE_OFICIALA')]}),

    ('Care este locația sediului ASE?', {'entities': [(10, 26, 'LOCATIE_SEDIU')]}),
    ('Unde se află adresa sediului ASE?', {'entities': [(13, 28, 'LOCATIE_SEDIU')]}),
    ('Cum ajung la locația sediului ASE?', {'entities': [(13, 29, 'LOCATIE_SEDIU')]}),
    ('locatia sediului ASE', {'entities': [(0, 16, 'LOCATIE_SEDIU')]}),
    ('adresa ASE', {'entities': [(0, 6, 'LOCATIE_SEDIU')]}),
    ('sediul ASE unde', {'entities': [(0, 6, 'LOCATIE_SEDIU')]}),
    ('locatie ASE', {'entities': [(0, 7, 'LOCATIE_SEDIU')]}),
    ('sediul ASE', {'entities': [(0, 6, 'LOCATIE_SEDIU')]}),
    ('adresa', {'entities': [(0, 6, 'LOCATIE_SEDIU')]}),
    ('locatie', {'entities': [(0, 7, 'LOCATIE_SEDIU')]}),
    ('ASE locatie sediu', {'entities': [(4, 17, 'LOCATIE_SEDIU')]}),
    ('unde este ASE', {'entities': [(0, 9, 'LOCATIE_SEDIU')]}),
    ('ASE adresa exacta', {'entities': [(4, 17, 'LOCATIE_SEDIU')]}),
    ('sediul central ASE', {'entities': [(0, 14, 'LOCATIE_SEDIU')]}),
    ('ASE coordonate sediu', {'entities': [(4, 20, 'LOCATIE_SEDIU')]}),
    ('locatia exacta ASE', {'entities': [(0, 14, 'LOCATIE_SEDIU')]}),
    ('adresa sediului central', {'entities': [(0, 23, 'LOCATIE_SEDIU')]}),
    ('ASE punct reper', {'entities': [(4, 15, 'LOCATIE_SEDIU')]}),
    ('ASE zona sediu', {'entities': [(4, 14, 'LOCATIE_SEDIU')]}),
    ('ASE harta sediu', {'entities': [(4, 15, 'LOCATIE_SEDIU')]}),

    ('Pagina web ASE?', {'entities': [(0, 10, 'SITE_WEB')]}),
    ('Website-ul ASE este?', {'entities': [(0, 10, 'SITE_WEB')]}),
    ('Adresa online a ASE?', {'entities': [(0, 13, 'SITE_WEB')]}),
    ('Care este adresa web oficială pentru informații ASE?', {'entities': [(10, 29, 'SITE_WEB')]}),
    ('Unde pot accesa resursele digitale ale ASE?', {'entities': [(16, 34, 'SITE_WEB')]}),
    ('Pagina de start ASE poate fi accesată?', {'entities': [(0, 15, 'SITE_WEB')]}),
    ('Site-ul oficial ASE?', {'entities': [(0, 15, 'SITE_WEB')]}),
    ('Acces la portalul ASE?', {'entities': [(9, 17, 'SITE_WEB')]}),
    ('Platforma online ASE este la ce adresă?', {'entities': [(0, 16, 'SITE_WEB')]}),
    ('site ASE', {'entities': [(0, 4, 'SITE_WEB')]}),
    ('ASE web', {'entities': [(4, 7, 'SITE_WEB')]}),
    ('pagina ASE', {'entities': [(0, 6, 'SITE_WEB')]}),
    ('ASE online', {'entities': [(4, 10, 'SITE_WEB')]}),
    ('adresa ASE', {'entities': [(0, 6, 'SITE_WEB')]}),
    ('website ASE', {'entities': [(0, 7, 'SITE_WEB')]}),
    ('portal ASE', {'entities': [(0, 6, 'SITE_WEB')]}),
    ('ASE digital', {'entities': [(4, 11, 'SITE_WEB')]}),
    ('ASE site', {'entities': [(4, 8, 'SITE_WEB')]}),
    ('web ASE', {'entities': [(0, 3, 'SITE_WEB')]}),
    ('online ASE', {'entities': [(0, 6, 'SITE_WEB')]}),
    ('ASE pagina', {'entities': [(4, 10, 'SITE_WEB')]}),
    ('ASE adresă', {'entities': [(4, 10, 'SITE_WEB')]}),
    ('cum accesez ASE online?', {'entities': [(16, 22, 'SITE_WEB')]}),
    ('pagina principala ASE', {'entities': [(0, 17, 'SITE_WEB')]}),
    ('site informatii ASE', {'entities': [(0, 15, 'SITE_WEB')]}),
    ('acces web ASE', {'entities': [(0, 9, 'SITE_WEB')]}),
    ('ASE pe internet', {'entities': [(4, 15, 'SITE_WEB')]}),
    ('unde gasesc site-ul ASE?', {'entities': [(12, 19, 'SITE_WEB')]}),
    ('ASE resurse online', {'entities': [(4, 18, 'SITE_WEB')]}),
    ('platforma ASE', {'entities': [(0, 9, 'SITE_WEB')]}),
    ('ASE URL', {'entities': [(4, 7, 'SITE_WEB')]}),
    ('website informativ ASE', {'entities': [(0, 18, 'SITE_WEB')]}),
    ('portal informatii ASE', {'entities': [(0, 17, 'SITE_WEB')]}),
    ('acces ASE digital', {'entities': [(10, 17, 'SITE_WEB')]}),
    ('pagina web informatii ASE', {'entities': [(7, 21, 'SITE_WEB')]}),
    ('site-ul ASE disponibil?', {'entities': [(0, 7, 'SITE_WEB')]}),
    ('ASE web oficial', {'entities': [(4, 15, 'SITE_WEB')]}),
]


# Function to augment data using RoWordNet synonyms
def augment_data_with_synonyms(data):
    augmented_data = []
    for text, annotations in data:
        spans = annotations['entities']
        for start, end, label in spans:
            term = text[start:end]
            synset_ids = wn.synsets(literal=term)

            synonyms = set()
            for synset_id in synset_ids:
                synset = wn.synset(synset_id)
                # Directly access the literals attribute and replace underscores
                literals = [literal.replace('_', ' ') for literal in synset.literals]
                for literal in literals:
                    if literal != term:
                        synonyms.add(literal)

            # Create augmented texts
            for synonym in synonyms:
                new_text = text[:start] + synonym + text[end:]
                new_start = start
                new_end = new_start + len(synonym)
                new_annotations = {'entities': [(new_start, new_end, label)]}
                augmented_data.append((new_text, new_annotations))

        # Always include the original text
        augmented_data.append((text, annotations))

    return augmented_data


# Augment the training data
augmented_TRAIN_DATA = augment_data_with_synonyms(TRAIN_DATA)

# Display augmented data
for example in augmented_TRAIN_DATA:
    print(example)