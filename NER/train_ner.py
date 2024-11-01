from spacy.util import minibatch
from thinc.schedules import compounding
from train_data import TRAIN_DATA
import random
import spacy
from spacy.training import Example
from spacy.pipeline import EntityRuler
from spacy.scorer import Scorer
from rowordnet import RoWordNet
import json

# Loading the model
nlp = spacy.load("ro_core_news_sm")
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner", last=True)
else:
    ner = nlp.get_pipe("ner")

def augment_data_with_synonyms(data):
    wn = RoWordNet()
    augmented_data = []
    print("Starting augmentation...")  #
    for text, annotations in data:
        original_data_length = len(augmented_data)
        spans = annotations['entities']
        for start, end, label in spans:
            term = text[start:end]
            synset_ids = wn.synsets(literal=term)
            synonyms = set()
            for synset_id in synset_ids:
                synset = wn.synset(synset_id)
                literals = [literal.replace('_', ' ') for literal in synset.literals]
                for literal in literals:
                    if literal != term:
                        synonyms.add(literal)
            for synonym in synonyms:
                new_text = text[:start] + synonym + text[end:]
                new_start = start
                new_end = new_start + len(synonym)
                new_annotations = {'entities': [(new_start, new_end, label)]}
                augmented_data.append((new_text, new_annotations))
        augmented_data.append((text, annotations))
        if len(augmented_data) > original_data_length:
            print(f"Added {len(augmented_data) - original_data_length} new sentences for: {text}")
    return augmented_data

TRAIN_DATA = augment_data_with_synonyms(TRAIN_DATA)
print(f"Total training instances: {len(TRAIN_DATA)}")

patterns = [
    {"label": "INTREBARI", "pattern": [{"LOWER": "intrebari"}]},
    {"label": "INTREBARI", "pattern": [{"LOWER": "faq"}]},
    {"label": "INTREBARI", "pattern": [{"TEXT": "Întrebări"}]},

    {"label": "ATRIBUTII_COMISIA_ETICA", "pattern": [{"LOWER": "atributii"}, {"LOWER": "comisia"}, {"LOWER": "de"}, {"LOWER": "etica"}]},
    {"label": "ATRIBUTII_COMISIA_ETICA", "pattern": [{"LOWER": "responsabilitati"}, {"LOWER": "comisia"}, {"LOWER": "de"}, {"LOWER": "etica"}]},
    {"label": "ATRIBUTII_COMISIA_ETICA", "pattern": [{"LOWER": "roluri"}, {"LOWER": "comisia"}, {"LOWER": "de"}, {"LOWER": "etica"}]},

    {"label": "COMPOZITIE_COMISIA_ETICA", "pattern": [{"LOWER": "membrii"}, {"LOWER": "comisiei"}, {"LOWER": "de"}, {"LOWER": "etica"}]},
    {"label": "COMPOZITIE_COMISIA_ETICA", "pattern": [{"LOWER": "structura"}, {"LOWER": "comisiei"}, {"LOWER": "de"}, {"LOWER": "etica"}]},
    {"label": "CONSTITUIRE_COMISIA_ETICA", "pattern": [{"LOWER": "formare"}, {"LOWER": "comisia"}, {"LOWER": "de"}, {"LOWER": "etica"}, {"LOWER": "si"}, {"LOWER": "deontologie"}]},

    {"label": "EXPRIMARE_LIBERA_OPINII", "pattern": [{"LOWER": "libertatea"}, {"LOWER": "de"}, {"LOWER": "exprimare"}]},
    {"label": "EXPRIMARE_LIBERA_OPINII", "pattern": [{"LOWER": "exprimare"}, {"LOWER": "libera"}]},
    {"label": "EXPRIMARE_LIBERA_OPINII", "pattern": [{"LOWER": "dreptul"}, {"LOWER": "la"}, {"LOWER": "exprimare"}]},
    {"label": "EXPRIMARE_LIBERA_OPINII",
     "pattern": [{"LOWER": "politici"}, {"LOWER": "exprimare"}, {"LOWER": "libera"}]},
    {"label": "EXPRIMARE_LIBERA_OPINII", "pattern": [{"LOWER": "protejarea"}, {"LOWER": "opiniei"}]},
    {"label": "EXPRIMARE_LIBERA_OPINII", "pattern": [{"LOWER": "reguli"}, {"LOWER": "exprimare"}]},

    {"label": "PARTENERI_ORGANIZATII", "pattern": [{"LOWER": "parteneri"}, {"LOWER": "ase"}]},
    {"label": "PARTENERI_ORGANIZATII", "pattern": [{"LOWER": "organizatii"}, {"LOWER": "colaboratoare"}]},
    {"label": "PARTENERI_ORGANIZATII", "pattern": [{"LOWER": "entitati"}, {"LOWER": "partenere"}]},
    {"label": "PARTENERI_ORGANIZATII", "pattern": [{"LOWER": "ase"}, {"LOWER": "si"}, {"LOWER": "parteneri"}]},
    {"label": "PARTENERI_ORGANIZATII", "pattern": [{"LOWER": "parteneriate"}]},
    {"label": "PARTENERI_ORGANIZATII", "pattern": [{"LOWER": "grupuri"}, {"LOWER": "suport"}]},

    {"label": "ORGANIZARE_PROGRAM_STUDII", "pattern": [{"LOWER": "prorectorul"}, {"LOWER": "si"}, {"LOWER": "programele"}, {"LOWER": "de"}, {"LOWER": "studii"}]},
    {"label": "ORGANIZARE_PROGRAM_STUDII", "pattern": [{"LOWER": "organizare"}, {"LOWER": "cursuri"}]},
    {"label": "ORGANIZARE_PROGRAM_STUDII", "pattern": [{"LOWER": "planificare"}, {"LOWER": "studii"}]},
    {"label": "ORGANIZARE_PROGRAM_STUDII", "pattern": [{"LOWER": "prorector"}, {"LOWER": "structurare"}, {"LOWER": "programe"}]},
    {"label": "ORGANIZARE_PROGRAM_STUDII", "pattern": [{"LOWER": "dezvoltare"}, {"LOWER": "curricula"}]},
    {"label": "ORGANIZARE_PROGRAM_STUDII", "pattern": [{"LOWER": "coordonare"}, {"LOWER": "programe"}, {"LOWER": "studii"}]},

    {"label": "EVIDENTA_STUDENTI", "pattern": [{"LOWER": "evidenta"}, {"LOWER": "studentilor"}]},
    {"label": "EVIDENTA_STUDENTI", "pattern": [{"LOWER": "registrul"}, {"LOWER": "studentilor"}]},
    {"label": "EVIDENTA_STUDENTI", "pattern": [{"LOWER": "gestionarea"}, {"LOWER": "studentilor"}]},
    {"label": "EVIDENTA_STUDENTI", "pattern": [{"LOWER": "inregistrarea"}, {"LOWER": "studentilor"}]},
    {"label": "EVIDENTA_STUDENTI", "pattern": [{"LOWER": "monitorizarea"}, {"LOWER": "studentilor"}]},
    {"label": "EVIDENTA_STUDENTI", "pattern": [{"LOWER": "administrarea"}, {"LOWER": "studentilor"}]},

    {"label": "STUDENTI_IMPLICARE_MANAGEMENT", "pattern": [{"LOWER": "implicarea"}, {"LOWER": "studentilor"}, {"LOWER": "in"}, {"LOWER": "management"}]},
    {"label": "STUDENTI_IMPLICARE_MANAGEMENT", "pattern": [{"LOWER": "participarea"}, {"LOWER": "studentilor"}, {"LOWER": "la"}, {"LOWER": "guvernanta"}]},
    {"label": "STUDENTI_IMPLICARE_MANAGEMENT", "pattern": [{"LOWER": "contributia"}, {"LOWER": "studentilor"}, {"LOWER": "la"}, {"LOWER": "decizii"}]},
    {"label": "STUDENTI_IMPLICARE_MANAGEMENT", "pattern": [{"LOWER": "rolul"}, {"LOWER": "studentilor"}, {"LOWER": "in"}, {"LOWER": "administratie"}]},
    {"label": "STUDENTI_IMPLICARE_MANAGEMENT", "pattern": [{"LOWER": "studenti"}, {"LOWER": "in"}, {"LOWER": "comitete"}, {"LOWER": "de"}, {"LOWER": "conducere"}]},
    {"label": "STUDENTI_IMPLICARE_MANAGEMENT", "pattern": [{"LOWER": "guvernanta"}, {"LOWER": "studenteasca"}, {"LOWER": "ase"}]},

    {"label": "VALIDARE_COMISIE_CONCURS", "pattern": [{"LOWER": "validare"}, {"LOWER": "comisii"}, {"LOWER": "ase"}]},
    {"label": "VALIDARE_COMISIE_CONCURS", "pattern": [{"LOWER": "procedura"}, {"LOWER": "validare"}, {"LOWER": "comisii"}]},
    {"label": "VALIDARE_COMISIE_CONCURS", "pattern": [{"LOWER": "confirmare"}, {"LOWER": "comisii"}, {"LOWER": "concurs"}]},
    {"label": "VALIDARE_COMISIE_CONCURS", "pattern": [{"LOWER": "etape"}, {"LOWER": "validare"}, {"LOWER": "comisii"}]},
    {"label": "VALIDARE_COMISIE_CONCURS", "pattern": [{"LOWER": "validarea"}, {"LOWER": "comisiei"}, {"LOWER": "examen"}]},
    {"label": "VALIDARE_COMISIE_CONCURS", "pattern": [{"LOWER": "comisii"}, {"LOWER": "examen"}, {"LOWER": "ase"}]},

    {"label": "CONTRACTE_MINISTER_RESORT", "pattern": [{"LOWER": "contracte"}, {"LOWER": "cu"}, {"LOWER": "ministerul"}, {"LOWER": "pentru"}, {"LOWER": "ase"}]},
    {"label": "CONTRACTE_MINISTER_RESORT", "pattern": [{"LOWER": "finantare"}, {"LOWER": "ase"}, {"LOWER": "prin"}, {"LOWER": "minister"}]},
    {"label": "CONTRACTE_MINISTER_RESORT", "pattern": [{"LOWER": "modalitati"}, {"LOWER": "de"}, {"LOWER": "finantare"}, {"LOWER": "ministeriala"}, {"LOWER": "ase"}]},
    {"label": "CONTRACTE_MINISTER_RESORT", "pattern": [{"LOWER": "gestionarea"}, {"LOWER": "finantarilor"}, {"LOWER": "ministeriale"}]},
    {"label": "CONTRACTE_MINISTER_RESORT", "pattern": [{"LOWER": "acorduri"}, {"LOWER": "ministeriale"}, {"LOWER": "pentru"}, {"LOWER": "finantare"}]},
    {"label": "CONTRACTE_MINISTER_RESORT", "pattern": [{"LOWER": "proceduri"}, {"LOWER": "contractuale"}, {"LOWER": "cu"}, {"LOWER": "ministerul"}]},

    {"label": "ADMITERE_PROGRAME_STUDII", "pattern": [{"LOWER": "admiterea"}, {"LOWER": "in"}, {"LOWER": "programele"}, {"LOWER": "de"}, {"LOWER": "studii"}, {"LOWER": "ase"}]},
    {"label": "ADMITERE_PROGRAME_STUDII", "pattern": [{"LOWER": "criterii"}, {"LOWER": "admitere"}, {"LOWER": "ase"}]},
    {"label": "ADMITERE_PROGRAME_STUDII", "pattern": [{"LOWER": "pasii"}, {"LOWER": "de"}, {"LOWER": "inscriere"}, {"LOWER": "ase"}]},
    {"label": "ADMITERE_PROGRAME_STUDII", "pattern": [{"LOWER": "procesare"}, {"LOWER": "aplicatii"}, {"LOWER": "ase"}]},
    {"label": "ADMITERE_PROGRAME_STUDII", "pattern": [{"LOWER": "documente"}, {"LOWER": "necesare"}, {"LOWER": "admitere"}]},
    {"label": "ADMITERE_PROGRAME_STUDII", "pattern": [{"LOWER": "admitere"}, {"LOWER": "internationali"}, {"LOWER": "ase"}]},

    {"label": "BENEFICIERE_SERVICII", "pattern": [{"LOWER": "servicii"}, {"LOWER": "studentesti"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_SERVICII", "pattern": [{"LOWER": "facilitati"}, {"LOWER": "studenti"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_SERVICII", "pattern": [{"LOWER": "ase"}, {"LOWER": "servicii"}, {"LOWER": "studenti"}]},
    {"label": "BENEFICIERE_SERVICII", "pattern": [{"LOWER": "acces"}, {"LOWER": "servicii"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_SERVICII", "pattern": [{"LOWER": "beneficii"}, {"LOWER": "studenti"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_SERVICII", "pattern": [{"LOWER": "servicii"}, {"LOWER": "academice"}, {"LOWER": "ase"}]},

    {"label": "LOCURI_FINANTATE_MARGINALIZATI", "pattern": [{"LOWER": "locuri"}, {"LOWER": "alocate"}, {"LOWER": "marginalizati"}]},
    {"label": "LOCURI_FINANTATE_MARGINALIZATI", "pattern": [{"LOWER": "finantare"}, {"LOWER": "pentru"}, {"LOWER": "studenti"}, {"LOWER": "marginalizati"}]},
    {"label": "LOCURI_FINANTATE_MARGINALIZATI", "pattern": [{"LOWER": "oportunitati"}, {"LOWER": "ase"}, {"LOWER": "pentru"}, {"LOWER": "marginalizati"}]},
    {"label": "LOCURI_FINANTATE_MARGINALIZATI", "pattern": [{"LOWER": "ase"}, {"LOWER": "sprijin"}, {"LOWER": "pentru"}, {"LOWER": "marginalizati"}]},
    {"label": "LOCURI_FINANTATE_MARGINALIZATI", "pattern": [{"LOWER": "ase"}, {"LOWER": "locuri"}, {"LOWER": "finantate"}, {"LOWER": "marginalizati"}]},
    {"label": "LOCURI_FINANTATE_MARGINALIZATI", "pattern": [{"LOWER": "burse"}, {"LOWER": "pentru"}, {"LOWER": "studenti"}, {"LOWER": "marginalizati"}]},

    {"label": "MOD_SOLUTIE", "pattern": [{"LOWER": "metode"}, {"LOWER": "rezolvare"}, {"LOWER": "dispute"}, {"LOWER": "ase"}]},
    {"label": "MOD_SOLUTIE", "pattern": [{"LOWER": "gestionare"}, {"LOWER": "conflicte"}, {"LOWER": "ase"}]},
    {"label": "MOD_SOLUTIE", "pattern": [{"LOWER": "strategii"}, {"LOWER": "solutii"}, {"LOWER": "ase"}]},
    {"label": "MOD_SOLUTIE", "pattern": [{"LOWER": "abordare"}, {"LOWER": "plangeri"}, {"LOWER": "ase"}]},
    {"label": "MOD_SOLUTIE", "pattern": [{"LOWER": "maniera"}, {"LOWER": "de"}, {"LOWER": "solutie"}, {"LOWER": "ase"}]},
    {"label": "MOD_SOLUTIE", "pattern": [{"LOWER": "ase"}, {"LOWER": "dispute"}]},

    {"label": "ALEGERE_REPREZENTANTI_STUDENTI", "pattern": [{"LOWER": "alegerea"}, {"LOWER": "reprezentantilor"}]},
    {"label": "ALEGERE_REPREZENTANTI_STUDENTI", "pattern": [{"LOWER": "selectia"}, {"LOWER": "reprezentantilor"}]},
    {"label": "ALEGERE_REPREZENTANTI_STUDENTI", "pattern": [{"LOWER": "procesul"}, {"LOWER": "de"}, {"LOWER": "selectie"}]},
    {"label": "ALEGERE_REPREZENTANTI_STUDENTI", "pattern": [{"LOWER": "criterii"}, {"LOWER": "alegeri"}]},
    {"label": "ALEGERE_REPREZENTANTI_STUDENTI", "pattern": [{"LOWER": "metoda"}, {"LOWER": "de"}, {"LOWER": "alegere"}]},
    {"label": "ALEGERE_REPREZENTANTI_STUDENTI", "pattern": [{"LOWER": "votarea"}, {"LOWER": "reprezentantilor"}]},

    {"label": "CONDITII_NORMALE_DIZABILITATI", "pattern": [{"LOWER": "conditii"}, {"LOWER": "pentru"}, {"LOWER": "studenti"}, {"LOWER": "cu"}, {"LOWER": "dizabilitati"}]},
    {"label": "CONDITII_NORMALE_DIZABILITATI", "pattern": [{"LOWER": "spatii"}, {"LOWER": "adaptate"}]},
    {"label": "CONDITII_NORMALE_DIZABILITATI", "pattern": [{"LOWER": "facilitati"}, {"LOWER": "pentru"}, {"LOWER": "dizabilitati"}]},
    {"label": "CONDITII_NORMALE_DIZABILITATI", "pattern": [{"LOWER": "acces"}, {"LOWER": "pentru"}, {"LOWER": "dizabilitati"}]},
    {"label": "CONDITII_NORMALE_DIZABILITATI", "pattern": [{"LOWER": "adaptari"}, {"LOWER": "pentru"}, {"LOWER": "dizabilitati"}]},
    {"label": "CONDITII_NORMALE_DIZABILITATI", "pattern": [{"LOWER": "ase"}, {"LOWER": "suport"}, {"LOWER": "pentru"}, {"LOWER": "studenti"}, {"LOWER": "cu"}, {"LOWER": "dizabilitati"}]},

    {"label": "ROL_STUDENTI_DESEMNARE_RECTOR", "pattern": [{"LOWER": "rolul"}, {"LOWER": "studentilor"}, {"LOWER": "in"}, {"LOWER": "desemnarea"}, {"LOWER": "rectorului"}]},
    {"label": "ROL_STUDENTI_DESEMNARE_RECTOR", "pattern": [{"LOWER": "influenta"}, {"LOWER": "studentilor"}, {"LOWER": "asupra"}, {"LOWER": "rectoratului"}]},
    {"label": "ROL_STUDENTI_DESEMNARE_RECTOR", "pattern": [{"LOWER": "votul"}, {"LOWER": "studentilor"}, {"LOWER": "pentru"}, {"LOWER": "rector"}]},
    {"label": "ROL_STUDENTI_DESEMNARE_RECTOR", "pattern": [{"LOWER": "selectia"}, {"LOWER": "rectorului"}, {"LOWER": "si"}, {"LOWER": "studentii"}]},
    {"label": "ROL_STUDENTI_DESEMNARE_RECTOR", "pattern": [{"LOWER": "impactul"}, {"LOWER": "voturilor"}, {"LOWER": "studentesti"}]},
    {"label": "ROL_STUDENTI_DESEMNARE_RECTOR", "pattern": [{"LOWER": "contributia"}, {"LOWER": "studentilor"}, {"LOWER": "la"}, {"LOWER": "desemnarea"}, {"LOWER": "rectorului"}]},

    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "ce"}, {"LOWER": "activitati"}, {"LOWER": "studentesti"}, {"LOWER": "sunt"}, {"LOWER": "incurajate"}, {"LOWER": "de"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "activitatile"}, {"LOWER": "extracurriculare"}, {"LOWER": "promovate"}, {"LOWER": "de"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "care"}, {"LOWER": "sunt"}, {"LOWER": "initiativele"}, {"LOWER": "studentesti"}, {"LOWER": "sustinute"}, {"LOWER": "de"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "activitati"}, {"LOWER": "studentesti"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "initiative"}, {"LOWER": "studentesti"}, {"LOWER": "sustinute"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "proiecte"}, {"LOWER": "studentesti"}, {"LOWER": "incurajate"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "evenimente"}, {"LOWER": "studentesti"}, {"LOWER": "promovate"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "activitati"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "proiecte"}, {"LOWER": "studentesti"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "evenimente"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "initiative"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "activitati"}, {"LOWER": "culturale"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "activitati"}, {"LOWER": "sportive"}, {"LOWER": "studentesti"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "workshop-uri"}, {"LOWER": "studentesti"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "conferinte"}, {"LOWER": "studentesti"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "ase"}, {"LOWER": "si"}, {"LOWER": "initiative"}, {"LOWER": "studentesti"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "programe"}, {"LOWER": "studentesti"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "cluburi"}, {"LOWER": "studentesti"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "voluntariat"}, {"LOWER": "studentesc"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "ase"}, {"LOWER": "incurajeaza"}, {"LOWER": "activitati"}, {"LOWER": "creative"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "parteneriate"}, {"LOWER": "studentesti"}, {"LOWER": "ase"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "activitati"}, {"LOWER": "de"}, {"LOWER": "cercetare"}, {"LOWER": "studentesti"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "ase"}, {"LOWER": "si"}, {"LOWER": "evenimente"}, {"LOWER": "culturale"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "activitati"}, {"LOWER": "academice"}, {"LOWER": "studentesti"}]},
    {"label": "INCURAJARE_ACTIVITATI", "pattern": [{"LOWER": "ase"}, {"LOWER": "si"}, {"LOWER": "dezvoltarea"}, {"LOWER": "studentilor"}]},

    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "cum"}, {"LOWER": "colaboreaza"}, {"LOWER": "ase"}, {"LOWER": "cu"}, {"LOWER": "comunitatea"}, {"LOWER": "locala"}, {"LOWER": "si"}, {"LOWER": "regionala"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "care"}, {"LOWER": "sunt"}, {"LOWER": "parteneriatele"}, {"LOWER": "ase"}, {"LOWER": "cu"}, {"LOWER": "comunitatea"}, {"LOWER": "locala"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "ce"}, {"LOWER": "initiative"}, {"LOWER": "comunitare"}, {"LOWER": "sustine"}, {"LOWER": "ase"}, {"LOWER": "in"}, {"LOWER": "regiune"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "cum"}, {"LOWER": "contribuie"}, {"LOWER": "ase"}, {"LOWER": "la"}, {"LOWER": "dezvoltarea"}, {"LOWER": "comunitatii"}, {"LOWER": "locale"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "ce"}, {"LOWER": "rol"}, {"LOWER": "joaca"}, {"LOWER": "ase"}, {"LOWER": "in"}, {"LOWER": "promovarea"}, {"LOWER": "dezvoltarii"}, {"LOWER": "regionale"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "colaborari"}, {"LOWER": "ase"}, {"LOWER": "cu"}, {"LOWER": "comunitatea"}, {"LOWER": "locala"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "parteneriatele"}, {"LOWER": "ase"}, {"LOWER": "cu"}, {"LOWER": "zona"}, {"LOWER": "locala"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "initiative"}, {"LOWER": "ase"}, {"LOWER": "in"}, {"LOWER": "comunitate"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "contributia"}, {"LOWER": "ase"}, {"LOWER": "la"}, {"LOWER": "comunitate"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "dezvoltarea"}, {"LOWER": "comunitara"}, {"LOWER": "prin"}, {"LOWER": "ase"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "ase"}, {"LOWER": "si"}, {"LOWER": "comunitatea"}, {"LOWER": "locala"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "ase"}, {"LOWER": "in"}, {"LOWER": "regiune"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "impactul"}, {"LOWER": "ase"}, {"LOWER": "asupra"}, {"LOWER": "comunitatii"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "proiecte"}, {"LOWER": "ase"}, {"LOWER": "cu"}, {"LOWER": "comunitatea"}]},
    {"label": "MISIUNE_COMUNITATE", "pattern": [{"LOWER": "ase"}, {"LOWER": "si"}, {"LOWER": "dezvoltarea"}, {"LOWER": "regionala"}]},

    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "cum"}, {"LOWER": "pot"}, {"LOWER": "studentii"}, {"LOWER": "ase"}, {"LOWER": "sa"}, {"LOWER": "beneficieze"}, {"LOWER": "de"}, {"LOWER": "asistenta"}, {"LOWER": "medicala"}, {"LOWER": "si"}, {"LOWER": "psihologica"}, {"LOWER": "gratuita"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "ce"}, {"LOWER": "servicii"}, {"LOWER": "de"}, {"LOWER": "sanatate"}, {"LOWER": "gratuita"}, {"LOWER": "sunt"}, {"LOWER": "disponibile"}, {"LOWER": "pentru"}, {"LOWER": "studentii"}, {"LOWER": "de"}, {"LOWER": "la"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "care"}, {"LOWER": "sunt"}, {"LOWER": "optiunile"}, {"LOWER": "de"}, {"LOWER": "asistenta"}, {"LOWER": "psihologica"}, {"LOWER": "pentru"}, {"LOWER": "studentii"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "cum"}, {"LOWER": "acceseaza"}, {"LOWER": "studentii"}, {"LOWER": "serviciile"}, {"LOWER": "de"}, {"LOWER": "consiliere"}, {"LOWER": "psihologica"}, {"LOWER": "oferite"}, {"LOWER": "de"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "ce"}, {"LOWER": "proceduri"}, {"LOWER": "trebuie"}, {"LOWER": "urmate"}, {"LOWER": "pentru"}, {"LOWER": "a"}, {"LOWER": "beneficia"}, {"LOWER": "de"}, {"LOWER": "asistenta"}, {"LOWER": "medicala"}, {"LOWER": "in"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "asistenta"}, {"LOWER": "medicala"}, {"LOWER": "gratuita"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "servicii"}, {"LOWER": "sanatate"}, {"LOWER": "studenti"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "consiliere"}, {"LOWER": "psihologica"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "beneficii"}, {"LOWER": "sanatate"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "acces"}, {"LOWER": "asistenta"}, {"LOWER": "psihologica"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "sanatate"}, {"LOWER": "gratuita"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "servicii"}, {"LOWER": "medicale"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "asistenta"}, {"LOWER": "psihiatrica"}, {"LOWER": "ase"}]},
    {"label": "BENEFICIERE_ASISTENTA_MEDICALA", "pattern": [{"LOWER": "suport"}, {"LOWER": "sanatate"}, {"LOWER": "studenti"}]},

    {"label": "DATA_MODIFICARE", "pattern": [{"LOWER": "cand"}, {"LOWER": "a"}, {"LOWER": "avut"}, {"LOWER": "loc"}, {"LOWER": "ultima"}, {"LOWER": "modificare"}, {"LOWER": "a"}, {"LOWER": "regulamentelor"}, {"LOWER": "ase"}]},
    {"label": "DATA_MODIFICARE", "pattern": [{"LOWER": "data"}, {"LOWER": "ultimei"}, {"LOWER": "modificari"}, {"LOWER": "a"}, {"LOWER": "statutelor"}, {"LOWER": "universitare"}, {"LOWER": "la"}, {"LOWER": "ase"}]},
    {"label": "DATA_MODIFICARE", "pattern": [{"LOWER": "cand"}, {"LOWER": "s-a"}, {"LOWER": "realizat"}, {"LOWER": "ultima"}, {"LOWER": "schimbare"}, {"LOWER": "in"}, {"LOWER": "regulamentul"}, {"LOWER": "ase"}]},
    {"label": "DATA_MODIFICARE", "pattern": [{"LOWER": "ultima"}, {"LOWER": "revizie"}, {"LOWER": "a"}, {"LOWER": "regulamentului"}, {"LOWER": "ase"}, {"LOWER": "a"}, {"LOWER": "fost"}, {"LOWER": "cand"}]},
    {"label": "DATA_MODIFICARE", "pattern": [{"LOWER": "care"}, {"LOWER": "este"}, {"LOWER": "data"}, {"LOWER": "ultimei"}, {"LOWER": "actualizari"}, {"LOWER": "a"}, {"LOWER": "normelor"}, {"LOWER": "ase"}]},

    {"label": "COLABORARE_VIZIUNE_MISIUNE", "pattern": [{"LOWER": "cum"}, {"LOWER": "se"}, {"LOWER": "manifesta"}, {"LOWER": "colaborarea"}, {"LOWER": "pentru"}, {"LOWER": "viziune"}, {"LOWER": "misiune"}, {"LOWER": "si"}, {"LOWER": "obiective"}, {"LOWER": "in"}, {"LOWER": "ase"}]},
    {"label": "COLABORARE_VIZIUNE_MISIUNE", "pattern": [{"LOWER": "ce"}, {"LOWER": "principii"}, {"LOWER": "orienteaza"}, {"LOWER": "colaborarea"}, {"LOWER": "pentru"}, {"LOWER": "viziunea"}, {"LOWER": "misiunea"}, {"LOWER": "si"}, {"LOWER": "obiectivele"}, {"LOWER": "ase"}]},
    {"label": "COLABORARE_VIZIUNE_MISIUNE", "pattern": [{"LOWER": "cum"}, {"LOWER": "contribuie"}, {"LOWER": "colaborarea"}, {"LOWER": "la"}, {"LOWER": "atingerea"}, {"LOWER": "viziunii"}, {"LOWER": "misiunii"}, {"LOWER": "si"}, {"LOWER": "obiectivelor"}, {"LOWER": "ase"}]},

    {"label": "PROPUNERE_COMISIE_ETICA", "pattern": [{"LOWER": "cum"}, {"LOWER": "se"}, {"LOWER": "propune"}, {"LOWER": "componența"}, {"LOWER": "comisiei"}, {"LOWER": "de"}, {"LOWER": "etica"}, {"LOWER": "in"}, {"LOWER": "ase"}]},
    {"label": "PROPUNERE_COMISIE_ETICA", "pattern": [{"LOWER": "care"}, {"LOWER": "sunt"}, {"LOWER": "criteriile"}, {"LOWER": "pentru"}, {"LOWER": "nominalizarea"}, {"LOWER": "comisiei"}, {"LOWER": "de"}, {"LOWER": "etica"}]},

    {"label": "ROL_STUDENTI_DESEMNARE_RECTOR", "pattern": [{"LOWER": "ce"}, {"LOWER": "rol"}, {"LOWER": "au"}, {"LOWER": "studentii"}, {"LOWER": "in"}, {"LOWER": "procesul"}, {"LOWER": "de"}, {"LOWER": "desemnare"}, {"LOWER": "a"}, {"LOWER": "rectorului"}, {"LOWER": "ase"}]},
    {"label": "ROL_STUDENTI_DESEMNARE_RECTOR", "pattern": [{"LOWER": "cum"}, {"LOWER": "influențeaza"}, {"LOWER": "studentii"}, {"LOWER": "alegerea"}, {"LOWER": "rectorului"}, {"LOWER": "in"}, {"LOWER": "ase"}]},

    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "care"}, {"LOWER": "sunt"}, {"LOWER": "etapele"}, {"LOWER": "aprobării"}, {"LOWER": "dezvoltării"}, {"LOWER": "bazei"}, {"LOWER": "materiale"}, {"LOWER": "în"}, {"LOWER": "ase"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "cum"}, {"LOWER": "se"}, {"LOWER": "inițiază"}, {"LOWER": "și"}, {"LOWER": "se"}, {"LOWER": "validează"}, {"LOWER": "extinderea"}, {"LOWER": "bazei"}, {"LOWER": "materiale"}, {"LOWER": "la"}, {"LOWER": "ase"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "ce"}, {"LOWER": "proceduri"}, {"LOWER": "urmează"}, {"LOWER": "pentru"}, {"LOWER": "consolidarea"}, {"LOWER": "bazei"}, {"LOWER": "materiale"}, {"LOWER": "în"}, {"LOWER": "ase"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "dezvoltare"}, {"LOWER": "baza"}, {"LOWER": "materiala"}, {"LOWER": "ase"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "extindere"}, {"LOWER": "baza"}, {"LOWER": "materiala"}, {"LOWER": "ase"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "consolidare"}, {"LOWER": "baza"}, {"LOWER": "materiala"}, {"LOWER": "ase"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "proiecte"}, {"LOWER": "dezvoltare"}, {"LOWER": "baza"}, {"LOWER": "materiala"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "planuri"}, {"LOWER": "extindere"}, {"LOWER": "baza"}, {"LOWER": "materiala"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "strategii"}, {"LOWER": "consolidare"}, {"LOWER": "baza"}, {"LOWER": "materiala"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "initiative"}, {"LOWER": "dezvoltare"}, {"LOWER": "baza"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "proiecte"}, {"LOWER": "extindere"}, {"LOWER": "baza"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "strategii"}, {"LOWER": "baza"}, {"LOWER": "materiala"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "procese"}, {"LOWER": "dezvoltare"}, {"LOWER": "baza"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "activitati"}, {"LOWER": "extindere"}, {"LOWER": "baza"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "proceduri"}, {"LOWER": "consolidare"}, {"LOWER": "baza"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "aprobare"}, {"LOWER": "dezvoltare"}, {"LOWER": "baza"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "validare"}, {"LOWER": "extindere"}, {"LOWER": "baza"}]},
    {"label": "DEZVOLTARE_BAZA_MATERIALA", "pattern": [{"LOWER": "sanctionare"}, {"LOWER": "consolidare"}, {"LOWER": "baza"}]},

    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "cum"}, {"LOWER": "pot"}, {"LOWER": "studentii"}, {"LOWER": "ase"}, {"LOWER": "sa"}, {"LOWER": "participe"}, {"LOWER": "la"}, {"LOWER": "procesul"}, {"LOWER": "de"}, {"LOWER": "elaborare"}, {"LOWER": "a"}, {"LOWER": "regulamentelor"}, {"LOWER": "universitare"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "ce"}, {"LOWER": "metode"}, {"LOWER": "sunt"}, {"LOWER": "disponibile"}, {"LOWER": "pentru"}, {"LOWER": "studentii"}, {"LOWER": "ase"}, {"LOWER": "pentru"}, {"LOWER": "a"}, {"LOWER": "contribui"}, {"LOWER": "la"}, {"LOWER": "elaborarea"}, {"LOWER": "regulamentelor"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "care"}, {"LOWER": "sunt"}, {"LOWER": "pasii"}, {"LOWER": "pentru"}, {"LOWER": "participarea"}, {"LOWER": "studentilor"}, {"LOWER": "ase"}, {"LOWER": "in"}, {"LOWER": "formularea"}, {"LOWER": "regulamentelor"}, {"LOWER": "academice"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "cum"}, {"LOWER": "sunt"}, {"LOWER": "implicati"}, {"LOWER": "studentii"}, {"LOWER": "ase"}, {"LOWER": "in"}, {"LOWER": "procesul"}, {"LOWER": "de"}, {"LOWER": "creare"}, {"LOWER": "a"}, {"LOWER": "regulilor"}, {"LOWER": "universitare"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "participare"}, {"LOWER": "la"}, {"LOWER": "regulamente"}, {"LOWER": "ase"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "contributia"}, {"LOWER": "studentilor"}, {"LOWER": "la"}, {"LOWER": "regulamente"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "implicare"}, {"LOWER": "studenti"}, {"LOWER": "in"}, {"LOWER": "regulamente"}, {"LOWER": "ase"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "studenti"}, {"LOWER": "ase"}, {"LOWER": "si"}, {"LOWER": "elaborarea"}, {"LOWER": "regulamentelor"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "ase"}, {"LOWER": "studenti"}, {"LOWER": "contributie"}, {"LOWER": "la"}, {"LOWER": "regulamente"}]},
    {"label": "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE", "pattern": [{"LOWER": "proces"}, {"LOWER": "elaborare"}, {"LOWER": "regulamente"}, {"LOWER": "ase"}]},
]

# Creating the EntityRuler and add patterns
ruler = EntityRuler(nlp)
ruler.add_patterns(patterns)
ruler.to_disk("./entity_ruler_patterns.jsonl")

if "entity_ruler" in nlp.pipe_names:
    nlp.remove_pipe("entity_ruler")
nlp.add_pipe("entity_ruler", before="ner").from_disk("./entity_ruler_patterns.jsonl")

# Adding entity labels to the NER component
for _, annotations in TRAIN_DATA:
    for ent in annotations.get("entities"):
        ner.add_label(ent[2])

def evaluate(ner_model, examples):
    scorer = Scorer()
    example_list = []
    for input_, annot in examples:
        doc = ner_model.make_doc(input_)
        example = Example.from_dict(doc, annot)
        example_pred = ner_model(input_)
        example_list.append(Example(example_pred, example.reference))
    scores = scorer.score(example_list)
    return scores

# Splitting the data into training and validation sets
random.shuffle(TRAIN_DATA)
split = int(len(TRAIN_DATA) * 0.8)
train_data = TRAIN_DATA[:split]
validation_data = TRAIN_DATA[split:]

# Get all unique entity types
entity_types = set()
for _, annotations in train_data:
    for ent in annotations.get("entities"):
        entity_types.add(ent[2])

# Function to create the CSV header
def create_csv_header(entity_types):
    headers = ["Iteration", "Loss", "Token Acc", "Token P", "Token R", "Token F", "Ents P", "Ents R", "Ents F"]
    for entity_type in entity_types:
        headers.extend([f"{entity_type} P", f"{entity_type} R", f"{entity_type} F"])
    return ",".join(headers)

# Create and write the CSV header
scores_file = "training_scores_detailed.csv"
with open(scores_file, mode='w', encoding='utf-8') as file:
    file.write(create_csv_header(entity_types) + "\n")

# Disabling other pipeline components during training
with nlp.disable_pipes(*[pipe for pipe in nlp.pipe_names if pipe != "ner"], "entity_ruler"):
    optimizer = nlp.begin_training()
    for itn in range(100):
        random.shuffle(train_data)
        losses = {}

        batches = minibatch(train_data, size=compounding(4., 64., 1.05))
        for batch in batches:
            examples = [Example.from_dict(nlp.make_doc(text), annots) for text, annots in batch]
            nlp.update(examples, drop=0.2, losses=losses)

        print(f"Losses at iteration {itn}: {losses}")

        # Evaluate the scores
        scores = evaluate(nlp, validation_data)
        print(f"Scores at iteration {itn}: {scores}")

        # Writing scores to the CSV
        with open(scores_file, mode='a', encoding='utf-8') as file:
            row = [itn, losses['ner'], scores['token_acc'], scores['token_p'], scores['token_r'],
                   scores['token_f'], scores['ents_p'], scores['ents_r'], scores['ents_f']]

            # Adding per-entity scores
            for entity_type in entity_types:
                ent_scores = scores['ents_per_type'].get(entity_type, {"p": 0, "r": 0, "f": 0})
                row.extend([ent_scores['p'], ent_scores['r'], ent_scores['f']])

            file.write(",".join(map(str, row)) + "\n")

model_path = r"E:\Licenta\NER_ASE_Model"
nlp.to_disk(model_path)
print(f"Model saved to {model_path}")