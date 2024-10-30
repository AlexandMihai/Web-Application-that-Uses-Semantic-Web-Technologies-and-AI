import re
from flask import Blueprint, request, render_template, session, jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from ..sparql import form_sparql_query, execute_sparql_query, entity_mapping
from ..ner import get_entities_from_ner
from ..database import get_db

bp = Blueprint('chat', __name__)

def get_current_user():
    try:
        verify_jwt_in_request(optional=True)
        return get_jwt_identity()
    except Exception as e:
        return None

def format_property_name(prop):
    # Special case for ASE to prevent it from being split
    if prop.lower() == "ase":
        return "ASE"

    # Removing the 'http://www.ase.ro#' prefix
    prop = re.sub(r'^http://www.ase.ro#', '', prop)

    # Dictionary
    compound_words = {
        "AutoplagiereRezultate": "Autoplagiere Rezultate",
        "ComercializareaLucrariStiintifice": "Comercializarea Lucrărilor Științifice",
        "ConfectieRezultateStiintifice": "Confecție Rezultate Științifice",
        "IncercarePromovareExamenMita": "Încercare de Promovare a Examenului prin Mită",
        "InformatiiFalseSolicitariGranturi": "Informații False în Solicitări de Granturi",
        "PlagiatDefinitie": "Definiția Plagiatului",
        "PlagiereRezultate": "Plagierea Rezultatelor",
        "SanctionareConducatorDoctoratVinovatie": "Sancționarea Conducătorului de Doctorat pentru Vinovăție",
        "SanctionareDisciplinarCadruDidactic": "Sancționare Disciplinară a Cadrelor Didactice",
        "SanctionareDoctorandTezaCopiataFalsificata": "Sancționare a Doctorandului pentru Teză Copiată sau Falsificată",
        "SanctionareExmatriculareCopiereFalsificare": "Sancționare prin Exmatriculare pentru Copiere sau Falsificare",
        "SanctionareExmatriculareFinalizareStudii": "Sancționare prin Exmatriculare la Finalizare Studii",
        "SanctionareRevocareFunctieConducere": "Sancționare prin Revocare a Funcției de Conducere"
    }

    # Returning from dictionary if present
    if prop in compound_words:
        return compound_words[prop]

    # Replacing special characters with their simpler forms
    prop = re.sub(r'([a-z])([A-Z])', r'\1 \2', prop)

    # Capitalizing
    formatted = ' '.join(word.capitalize() for word in prop.split())

    return formatted

@bp.route('/chat')
def chat():
    initial_message = {
        'type': 'response',
        'text': 'Dacă nu știi ce întrebare să pui, scrie „Întrebări” și o să te ajut cu câteva idei'
    }

    if 'chat_history' not in session:
        session['chat_history'] = [initial_message]
    elif not any(msg['text'] == initial_message['text'] for msg in session['chat_history']):
        session['chat_history'].append(initial_message)

    return render_template('chat.html', chat_history=session.get('chat_history', []))

@bp.route('/query', methods=['POST'])
def query():
    question = request.form.get('question')
    entities = get_entities_from_ner(question)
    print("Entities from NER model:", entities)
    sparql_query, identified_entity = form_sparql_query(entities)
    print("Generated SPARQL query:", sparql_query)
    print("Entity:", identified_entity)
    results_text = "Nu am putut găsi un răspuns la această întrebare."

    if identified_entity == "INTREBARI":
        import random
        import sys
        sys.path.append('E:\\Licenta\\NER')
        from train_data import TRAIN_DATA
        first_questions_by_entity = {}
        for question, annotation in TRAIN_DATA:
            for start, end, entity_type in annotation['entities']:
                if entity_type not in first_questions_by_entity:
                    first_questions_by_entity[entity_type] = question
        sample_entities = list(first_questions_by_entity.values())
        random_questions = random.sample(sample_entities, 3)
        results_text = "Ai mai jos câteva întrebări:<br>"
        for question in random_questions:
            safe_question = question.replace("'", "\\'")
            results_text += f'<a href="#" onclick="askQuestion(\'{safe_question}\')">{question}</a><br>'
    elif sparql_query:
        results = execute_sparql_query(sparql_query)
        print("Raw SPARQL results:", results)
        if results["results"]["bindings"]:
            result = results["results"]["bindings"][0]

            if identified_entity == "LEGE_INFIINTARE":
                lege = results["results"]["bindings"][0].get('lege', {}).get('value', 'N/A')
                results_text = f"Legea de înființare a ASE este {lege}."

            elif identified_entity == "NIVEL_ACREDITARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Nivelul de acreditare al universității este {val}."

            elif identified_entity == "CARACTER_UNIVERSITATE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Caracterul universității este {val}."

            elif identified_entity == "DENUMIRE_OFICIALA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Denumirea oficială a universității este {val}."

            elif identified_entity == "LOCATIE_SEDIU":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Sediul universității este {val}."

            elif identified_entity == "SITE_WEB":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Site-ul web al universității este {val}."

            elif identified_entity == "DENUMIRE_ENGLEZA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE este cunoscută ca {val}."

            elif identified_entity == "INFIINTARE_ASE":
                decretRegal = results["results"]["bindings"][0].get('decretRegal', {}).get('value', 'N/A')
                lege = results["results"]["bindings"][0].get('lege', {}).get('value', 'N/A')
                promulgator = results["results"]["bindings"][0].get('promulgator', {}).get('value', 'N/A')
                results_text = f"ASE a fost înființată conform decretului Regal {decretRegal}, prin {lege}, promulgată de {promulgator}."

            elif identified_entity == "PROMULGATOR":
                promulgator = results["results"]["bindings"][0].get('promulgator', {}).get('value', 'N/A')
                results_text = f"Legea de înființare a ASE a fost promulgată de {promulgator}."

            elif identified_entity == "DECRET_REGAL":
                decretRegal = results["results"]["bindings"][0].get('decretRegal', {}).get('value', 'N/A')
                results_text = f"Decretul regal de înființare a ASE este {decretRegal}."

            elif identified_entity == "DATA_SARBATOARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Data de sărbătoare a ASE este {val}."

            elif identified_entity == "TIP_DISCRIMINARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Tipurile de discriminări considerate abateri etice la ASE sunt: {val}."

            elif identified_entity == "ACTIVITATE_NENUMARATA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Da, este considerată o abatere etică." if val == "true" else "Nu, nu este considerată o abatere etică."

            elif identified_entity == "ABATERE_ETICA":
                abaterile = []
                for result in results["results"]["bindings"]:
                    prop = result['property']['value'].split("#")[-1]
                    val = result['value']['value']

                    formatted_prop = format_property_name(prop)

                    if val == "true":
                        abaterile.append(formatted_prop)
                    else:
                        abaterile.append(f"{formatted_prop}: {val}")
                results_text = "Abaterile etice includ: " + ', '.join(abaterile) + "."


            elif identified_entity == "ABATERE_GRAVA":

                abaterile_grave = []

                for result in results["results"]["bindings"]:
                    prop = result['property']['value'].split("#")[-1]  # Extracting the property name from the full URI
                    val = result['value']['value']

                    # Skip "Plagiat Definitie"
                    if prop == "PlagiatDefinitie":
                        continue

                    formatted_prop = format_property_name(prop)

                    if val == "true":
                        abaterile_grave.append(formatted_prop)
                results_text = "Abaterile grave includ: " + ', '.join(abaterile_grave) + "."

            elif identified_entity == "APROBATOR_SPATII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Spațiile pentru activitățile culturale educative și sportive sunt aprobate {val}."

            elif identified_entity == "INCURAJARE_ACTIVITATI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE promovează {val}."

            elif identified_entity == "PLANIFICARE_EVENIMENTE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Evenimentele culturale și sportive sunt planificate {val}."

            elif identified_entity == "TIP_EVENIMENTE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE găzduiește evenimente de tipul: {val}."

            elif identified_entity == "PARTENERI_ORGANIZATII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE colaborează cu organizații {val} pentru evenimentele sale."

            elif identified_entity == "RESPONSABIL_ORGANIZARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Responsabilitatea organizării evenimentelor revine {val}."

            elif identified_entity == "SUSTINERE_ACTIVITATI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE susține activitățile studențești {val}."

            elif identified_entity == "RATIFICATOR_CARTE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Modificările Cartei ASE sunt ratificate de {val}."

            elif identified_entity == "INITIATOR_AMENDA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"O amendă pentru Carta ASE poate fi propusă de {val}."

            elif identified_entity == "EXECUTOR_SANCTIUNI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Penalizările în ASE sunt aplicate de {val}."

            elif identified_entity == "TERMEN_SANCTIUNI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Sancțiunile trebuie aplicate într-un termen de {val}."

            elif identified_entity in ["AUTONOMIE_DIDACTICA", "AUTONOMIE_FINANCIARA", "AUTONOMIE_FUNCTIONALA"]:
                autonomie_details = []
                for result in results["results"]["bindings"]:
                    for prop in entity_mapping[identified_entity]["node_properties"]:
                        if f"{prop}" in result:
                            val = result[f"{prop}"]['value']
                            if val == "true":
                                autonomie_details.append(format_property_name(prop))

                if identified_entity == "AUTONOMIE_DIDACTICA":
                    autonomie_type = "didactică"
                elif identified_entity == "AUTONOMIE_FINANCIARA":
                    autonomie_type = "financiară"
                else:
                    autonomie_type = "funcțională"

                if autonomie_details:
                    results_text = f"Autonomia {autonomie_type} la ASE include: " + ', '.join(autonomie_details) + "."
                else:
                    results_text = f"Nu s-au găsit detalii despre autonomia {autonomie_type} la ASE."

            elif identified_entity == "CHELTUIELI_LEGE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Cheltuielile la ASE trebuie efectuate cu respectarea legii." if val == "true" else "Nu există informații specifice despre respectarea legii în cheltuieli."


            elif identified_entity == "DEZVOLTARE_BAZA_MATERIALA":

                val = results["results"]["bindings"][0]['value']['value']

                if "propun de către" in val:
                    val = val.replace("propun de către", "propusă de către")

                results_text = f"Dezvoltarea bazei materiale este {val}."

            elif identified_entity == "PRINCIPII_GESTIONARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Principiile care ghidează gestionarea resurselor la ASE includ prudențialitatea și transparența." if val == "true" else "Nu există principii specifice de gestionare a resurselor menționate."

            elif identified_entity == "UTILIZARE_SPONSORIZARI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Utilizarea resurselor din sponsorizări la ASE se face conform contractului." if val == "true" else "Nu există informații specifice despre utilizarea resurselor din sponsorizări."

            elif identified_entity == "MINIMIZARE_HARTUIRE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "ASE ia măsuri pentru a minimiza teama de hărțuire sexuală, prin implementarea unor politici clare și a unor programe de sensibilizare și educație, care includ sesiuni de formare, linii de raportare confidențiale și suport psihologic, asigurând astfel un mediu sigur și respectuos pentru toți membrii comunității academice." if val == "true" else "Nu există informații specifice despre minimizarea temerii de hărțuire sexuală."

            elif identified_entity == "MOD_SOLUTIE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Comisia de confidențialitate ASE folosește o metodă de soluționare {val}."

            elif identified_entity == "PROTEJARE_IDENTITATE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Identitatea victimelor este protejată în cadrul ASE, prin implementarea unor proceduri stricte de confidențialitate și securitate a datelor, care asigură anonimatul și integritatea informațiilor personale ale acestora." if val == "true" else "Nu există informații specifice despre protejarea identității victimelor."

            elif identified_entity == "ATRIBUTII_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Atribuțiile Comisiei de Etică a ASE includ: {val}."

            elif identified_entity == "COMPOZITIE_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Comisia de Etică în ASE este compusă conform următoarelor criterii: {val}."

            elif identified_entity == "CONSTITUIRE_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Comisia de Etică la ASE se constituie ca {val}."

            elif identified_entity == "EXCLUDERE_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Următoarele persoane sunt excluse din Comisia de Etică a ASE: {val}."

            elif identified_entity == "HOTARARI_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Hotărârile Comisiei de Etică de la ASE sunt avizate astfel: {val}."

            elif identified_entity == "ATRIBUTII_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Atribuțiile Comisiei de Etică a ASE includ: {val}."

            elif identified_entity == "COMPOZITIE_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Comisia de Etică în ASE este compusă conform următoarelor criterii: {val}."

            elif identified_entity == "CONSTITUIRE_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Comisia de Etică și Deontologie Universitară la ASE se constituie ca: {val}."

            elif identified_entity == "EXCLUDERE_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Următoarele persoane sunt excluse din Comisia de Etică a ASE: {val}."

            elif identified_entity == "HOTARARI_COMISIA_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Hotărârile Comisiei de Etică de la ASE sunt avizate astfel: {val}."

            elif identified_entity == "CALITATE_CERCETATOR_POSTDOCTORAT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Calificările necesare pentru un cercetător postdoctorat în ASE sunt: {val}."

            elif identified_entity == "CALITATE_CURSANT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Categoria cursanților în ASE include: {val}."

            elif identified_entity == "CALITATE_PERSONAL_DIDACTIC":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Calitatea personalului didactic în ASE este definită ca: {val}."

            elif identified_entity == "CALITATE_STUDENTI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Statutul studenților în ASE este stabilit prin: {val}."

            elif identified_entity == "ATRIBUTII_PERSONAL":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Atribuțiile personalului universitar la ASE sunt stabilite astfel: {val}."

            elif identified_entity == "COLABORARE_VIZIUNE_MISIUNE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Colaborarea pentru viziune, misiune și obiective în ASE este promovată activ, prin organizarea de sesiuni de brainstorming, ateliere și conferințe care implică toate părțile interesate, asigurând astfel alinierea tuturor membrilor comunității academice la valorile și obiectivele instituției." if val == "true" else "Nu există informații specifice despre colaborare pentru viziune, misiune și obiective."

            elif identified_entity == "DIALOG_SOCIAL":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Dialogul social în ASE este promovat activ, prin inițierea de forumuri de discuție, întâlniri periodice și grupuri de lucru care facilitează schimbul de idei și feedback între studenți, cadre didactice și personal administrativ, contribuind la un mediu academic deschis și colaborativ." if val == "true" else "Nu există informații specifice despre promovarea dialogului social."

            elif identified_entity == "EQUIVALARE_FUNCTII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"{val}."


            elif identified_entity == "STRUCTURARE_COMUNITATE":

                structurare_details = []

                seen_details = set()
                for result in results["results"]["bindings"]:
                    details = []

                    for prop in entity_mapping[identified_entity]["node_properties"]:
                        if f"{prop}" in result:
                            formatted_prop_name = format_property_name(prop)
                            detail = f"{formatted_prop_name}: {result[f'{prop}']['value']}"
                            details.append(detail)

                    details_tuple = tuple(details)

                    if details_tuple not in seen_details:
                        seen_details.add(details_tuple)
                        structurare_details.extend(details)

                if structurare_details:
                        results_text = "Structurarea comunității universitare din ASE include: " + '; '.join(structurare_details) + "."

                else:
                        results_text = "Nu s-au găsit detalii despre structurarea comunității universitare din ASE."

            elif identified_entity == "STRUCTURA_CERCETATORI_POSTDOCTORAT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Structura cercetătorilor postdoctorat în ASE: {val}."

            elif identified_entity == "STRUCTURA_CURSANTI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Structura cursanților în ASE: {val}."

            elif identified_entity == "STRUCTURA_PERSONAL_DIDACTIC":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Structura personalului didactic în ASE: {val}."

            elif identified_entity == "STRUCTURA_PERSONAL_DIDACTIC_AUXILIAR":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Structura personalului didactic auxiliar în ASE: {val}."

            elif identified_entity == "STRUCTURA_STUDENTI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Structura studenților în ASE: {val}."

            elif identified_entity == "CONFLICT_INTERESE_DECIZII_ACTE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Se consideră un conflict de interese în deciziile sau actele ASE când sunt {val}."

            elif identified_entity == "INCOMPATIBILITATI_CONFLICT_INTERESE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Incompatibilitățile ce pot genera un conflict de interese în ASE includ: {val}."

            elif identified_entity == "INFLUENTA_INDEPLINIRE_ATRIBUTII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Pentru a evita conflictele de interese în ASE, influențarea îndeplinirii atribuțiilor trebuie să fie {val}."

            elif identified_entity == "INTERES_PERSONAL":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Interesul personal în contextul unui conflict de interese la ASE reprezintă {val}."

            elif identified_entity == "OBLIGATIE_INFORMARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Obligația de informare în cazul unui conflict de interese în ASE este să {val}."

            elif identified_entity == "SITUATIE_CONFLICT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"O situație de conflict de interese în ASE este definită când {val}."

            elif identified_entity == "VERIFICARE_CONFLICT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Verificarea situațiilor de conflict de interese în ASE este realizată de {val}."

            elif identified_entity == "ANALIZA_PLANURI_INVATAMANT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Planurile de învățământ în ASE se {val}."

            elif identified_entity == "APROBARE_CERERI_CONCEDII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Cererile de concedii pentru specializare sau cercetare în ASE sunt aprobate de {val}."

            elif identified_entity == "APROBARE_CONCURS_POSTURI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Se {val}."

            elif identified_entity == "APROBARE_OPERATIUNI_FINANCIARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Operațiunile financiare majore în ASE sunt aprobate de {val}."

            elif identified_entity == "AVIZARE_EXAMEN_MEDICAL":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Se {val}."

            elif identified_entity == "AVIZARE_RAPORT_REGIE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Raportul Rectorului privind cheltuielile pentru granturi în ASE este avizat astfel: {val}."

            elif identified_entity == "ELABORARE_BUGET_BILANT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Bugetul și bilanțul anual în ASE sunt elaborați și întocmiți de {val}."


            elif identified_entity == "ELABORARE_REGULAMENTE_METODOLOGII":

                regulamente_details = set()  # Using a set to not store duplicates

                for result in results["results"]["bindings"]:
                    for prop in entity_mapping[identified_entity]["node_properties"]:

                        if f"{prop}" in result:
                            formatted_prop = format_property_name(prop)
                            regulamente_details.add(formatted_prop)

                if regulamente_details:
                        results_text = "Regulamentele și metodologiile în ASE sunt elaborate astfel: " + ', '.join(
                        sorted(regulamente_details)) + "."

                else:

                    results_text = "Nu s-au găsit detalii despre elaborarea regulamentelor și metodologiilor în ASE."

            elif identified_entity == "INDEPLINIRE_ALTE_ATRIBUTII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Consiliul de Administrație în ASE {val}."

            elif identified_entity == "ORGANIZARE_CONCURS_DIRECTOR":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Concursul pentru Director General Administrativ în ASE este organizat astfel: {val}."

            elif identified_entity == "PROPUNERE_AN_SABATIC":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Propunerea acordării anului sabatic în ASE este făcută de {val}."

            elif identified_entity == "PROPUNERE_COMISIE_ETICA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Componența Comisiei de Etică în ASE este propusă astfel: {val}."


            elif identified_entity == "STABILIRE_PARTENERIATE":
                val = results["results"]["bindings"][0]['value']['value']
                val = val.replace('stabilește', 'stabilite prin')
                results_text = f"Parteneriatele în ASE sunt {val}."

            elif identified_entity == "VALIDARE_COMISIE_CONCURS":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Comisiile de concurs și examen în ASE sunt validate de {val}."

            elif identified_entity == "ALEGERI_CONSILIUL_DEPARTAMENTULUI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Membrii Consiliului Departamentului în ASE sunt aleși prin {val}."

            elif identified_entity == "REGULAMENT_CONSILIUL_DEPARTAMENTULUI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Există un regulament propriu pentru Consiliul Departamentului în ASE: {val}."

            elif identified_entity == "ALEGERI_CONSILIUL_FACULTATII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Membrii Consiliului Facultății în ASE sunt aleși prin {val}."

            elif identified_entity == "ATRIBUTII_CONSILIUL_FACULTATII":
                strategii = results["results"]["bindings"][0].get('propunereStrategii', {}).get('value', 'N/A')
                results_text = f"Atribuțiile Consiliului Facultății în ASE includ propunerea de {strategii}."

            elif identified_entity == "COMPOZITIE_CONSILIUL_FACULTATII":
                personal_didactic = results["results"]["bindings"][0].get('reprezentantiPersonalDidactic', {}).get(
                    'value', 'N/A')
                studenti = results["results"]["bindings"][0].get('reprezentantiStudenti', {}).get('value', 'N/A')
                results_text = f"Consiliul Facultății în ASE este compus din reprezentanți ai personalului didactic: {personal_didactic} și studenți: {studenti}."

            elif identified_entity == "CONDITII_MEMBRI_PERSONAL_DIDACTIC":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Condițiile pentru membrii personalului didactic în Consiliul Facultății ASE sunt: {val}."

            elif identified_entity == "CONDITII_MEMBRI_STUDENTI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Condițiile pentru membrii studenți în Consiliul Facultății ASE sunt: {val}."

            elif identified_entity == "QUORUM_CONSILIUL_FACULTATII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Quorumul necesar pentru Consiliul Facultății în ASE este de {val}."

            elif identified_entity == "SEDINTE_CONDUCERE_CONSILIUL_FACULTATII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Ședințele Consiliului Facultății în ASE sunt conduse de {val}."

            elif identified_entity == "SEDINTE_FRECVENTA_CONSILIUL_FACULTATII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Frecvența ședințelor Consiliului Facultății în ASE este {val}."

            elif identified_entity == "VOT_CONSILIUL_FACULTATII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Votul în Consiliul Facultății din ASE se realizează prin majoritatea {val}."

            elif identified_entity == "ALEGERI_CONSILIUL_SCOLII_DOCTORALE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Membrii Consiliului Școlii Doctorale în ASE sunt aleși prin {val}."

            elif identified_entity == "REGULAMENT_CONSILIUL_SCOLII_DOCTORALE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Funcționarea Consiliului Școlii Doctorale în ASE se bazează pe {val}."


            elif identified_entity == "ATRIBUTII_C_S_U_DOCTORAT":

                attributions = []

                seen_attributions = set()
                for result in results["results"]["bindings"]:
                    for prop in entity_mapping[identified_entity]["node_properties"]:

                        if f"{prop}" in result:
                            formatted_prop_name = format_property_name(prop)
                            value = result[f"{prop}"]['value']
                            attribution = f"{formatted_prop_name}: {value}"

                            if attribution not in seen_attributions:
                                seen_attributions.add(attribution)
                                attributions.append(attribution)

                if attributions:
                    results_text = "Atribuțiile Consiliului Studiilor Universitare de Doctorat în ASE includ: " + '; '.join(attributions) + "."
                else:
                    results_text = "Nu s-au găsit detalii despre atribuțiile Consiliului Studiilor Universitare de Doctorat în ASE."

            elif identified_entity == "COORDONARE_PARTENERIATE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Parteneriatele pentru școlile doctorale în ASE sunt coordonate astfel: {val}."

            elif identified_entity == "CONDITII_MEMBRI_CADRE_DIDACTICE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Cadrele didactice ale Consiliului Studiilor Universitare de Doctorat pot include {val}."

            elif identified_entity == "DESEMNARE_DIRECTOR":
                desemnare = None
                functie_asimilata = None

                # Looping through the results to find the properties
                for result in results["results"]["bindings"]:
                    if 'desemnare' in result:
                        desemnare = result['desemnare']['value']
                    if 'functieAsimilata' in result:
                        functie_asimilata = result['functieAsimilata']['value']

                # Constructing the response text based on the available information
                responses = []
                if desemnare:
                    responses.append(f"Directorul este {desemnare}")
                if functie_asimilata == "true":
                    responses.append("Funcția directorului este asimilată celei de prorector.")
                elif functie_asimilata == "false":
                    responses.append("Funcția directorului nu este asimilată celei de prorector.")

                results_text = " ".join(responses) if responses else "Nu s-au găsit detalii despre desemnarea directorului."

            elif identified_entity == "MANDAT_CADRE_DIDACTICE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Mandatul cadrelor didactice în cadrul Consiliului Studiilor Universitare de Doctorat este de {val}."

            elif identified_entity == "NUMAR_MEMBRI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Consiliul Studiilor Universitare de Doctorat în ASE este format din {val} persoane."

            elif identified_entity == "DATA_APROBARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Ultima modificare în ASE a fost aprobată la data de {val}."

            elif identified_entity == "DATA_MODIFICARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Ultima modificare a regulamentelor ASE a avut loc la data de {val}."

            elif identified_entity == "VIGOARE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Modificările ASE intră în vigoare {val}."

            elif identified_entity == "MEMBRU_DREPT_CONSILIU_ADMINISTRATIE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Decanul este membru de drept în Consiliul de Administrație al ASE." if val == "true" else "Decanul nu este membru de drept în Consiliul de Administrație al ASE."

            elif identified_entity == "SITUATII_DEMISIE_DECAN":
                demisie_details = []
                de = None

                for result in results["results"]["bindings"]:
                    if 'de' in result:
                        de = result['de']['value']

                    for situatie in ["incalcareCodEticaDeontologie", "incalcareLegislatieNormeEtica",
                                     "incompatibilitateLegal", "neindeplinireIndicatoriPerformanta",
                                     "neindeplinireSarcini", "prejudiciuInteresePrestigiuASE"]:

                        if situatie in result:
                            situatie_val = result[situatie]['value']
                            if situatie_val == "true":
                                formatted_situatie = format_property_name(situatie)
                                demisie_details.append(formatted_situatie)

                if de: demisie_details.insert(0,
                                              f"Decanul poate fi demis de {de}, în urma consultării Consiliului facultății")

                results_text = "; ".join(demisie_details) if demisie_details else "Nu s-au găsit detalii specifice despre situațiile de demisie a Decanului."

            elif identified_entity == "RESPONSABILITATI_MANAGEMENT_FACULTATE":

                val = results["results"]["bindings"][0]['value']['value']
                if val == 'true':
                    results_text = "Decanul are responsabilități semnificative în gestionarea facultății, supervizând activitățile administrative, financiare și academice."
                else:
                    results_text = "Decanul nu deține responsabilități semnificative în gestionarea facultății sau aceste responsabilități sunt limitate la funcții specifice și mai puțin influente."


            elif identified_entity == "SARCINI_DECAN":
                sarcini_details = []
                for result in results["results"]["bindings"]:
                    for sarcina in ["anulareRezultatEvaluare", "aplicareHotarari", "avizeazaFisaPostului",
                                    "conducereSedinteConsiliulFacultatii", "indeplinesteSarciniStabilite",
                                    "numireProdecani", "prezintaRapoarteConsiliuAdministratie",
                                    "prezintaRapoarteConsiliuFacultate", "propuneSancțiuniDisciplinare",
                                    "publicaDecizii", "raspundeAngajareEvaluarePersonal",
                                    "raspundeConcursuriOcuparePosturi", "raspundeManagementCalitateFinanciar",
                                    "semneazaActeDiplome"]:

                        if sarcina in result:
                            sarcina_val = result[sarcina]['value']

                            if sarcina_val == "true":
                                formatted_sarcina = format_property_name(sarcina)
                                sarcini_details.append(formatted_sarcina)

                results_text = "Sarcinile Decanului în cadrul facultății din ASE includ: " + ", ".join(sarcini_details) if sarcini_details else "Nu s-au găsit detalii specifice despre sarcinile Decanului."


            elif identified_entity == "SELECTIE_DECAN":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Selectarea Decanului facultății în ASE se face prin {val}."

            elif identified_entity == "ASUMARE_OBLIGATII_DEONTOLOGIA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Asumarea obligațiilor în cadrul deontologiei universitare ASE presupune {val}."

            elif identified_entity == "DEMNITATE_CONDUITA_DEONTOLOGIA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Demnitatea și conduita în deontologia universitară ASE se caracterizează prin {val}."

            elif identified_entity == "PRODUCEREA_CUNOASTERII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Producerea cunoașterii în departamentele ASE se asigură {val}."

            elif identified_entity == "CONDUCERE_DEPARTAMENT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Un departament în ASE este condus {val}."

            elif identified_entity == "INFIINTARE_DEPARTAMENT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Departamentele în ASE {val}."

            elif identified_entity == "STRUCTURA_DEPARTAMENT":
                structura_details = []
                for result in results["results"]["bindings"]:
                    for prop in entity_mapping[identified_entity]["node_properties"]:
                        if f"{prop}" in result:
                            prop_value = result[f"{prop}"]['value']
                            formatted_prop = format_property_name(prop)
                            structura_details.append(formatted_prop)

                if structura_details:
                    results_text = "Structurile incluse în cadrul unui departament ASE includ: " + ', '.join(
                        structura_details) + "."
                else:
                    results_text = "Nu s-au găsit detalii despre structurile unui departament ASE."

            elif identified_entity == "FUNCTIE_DIRECTOR_CSUD":
                results_text = "Funcția de conducere ocupată de Directorul CSUD în ASE include diverse responsabilități și atribuții."

            elif identified_entity == "CONDUCE_COMPONENTE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Directorul General Adjunct conduce componentele structurii administrative ASE {val}."



            elif identified_entity == "SUBORDONAT_DIRECTOR_GENERAL":
                val = results["results"]["bindings"][0]['value']['value']
                # Extracting the last part of the URI after the '#'
                readable_name = val.split('#')[-1]
                readable_name = format_property_name(readable_name)
                readable_name = readable_name.replace('Director', 'Directorului')

                results_text = f"Directorul General Adjunct Administrativ în ASE este subordonat {readable_name}."

            elif identified_entity == "CONDUCE_STRUCTURA_ADMINISTRATIVA":
                val = results["results"]["bindings"][0]['value']['value']
                if val == "true":
                    results_text = f"Structura administrativă ASE este condusă de Directorul General Administrativ."
                else:
                    results_text = "Nu s-a găsit detalii despre conducerea structurii administrative."

            elif identified_entity == "OCUPARE_POST_DIRECTOR_GENERAL":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Postul de Director General Administrativ în ASE se ocupă prin {val}."

            elif identified_entity == "SITUATII_DEMISIE_DIRECTOR_GENERAL":
                de = results["results"]["bindings"][0].get('de', {}).get('value', 'N/A')
                situatii_props = ["incalcareLegislatieNormeEtica", "neindeplinireSarcini", "prejudiciuIntereseASE"]
                situatii_readable = [format_property_name(prop) for prop in situatii_props]
                situatii_text = ", ".join(situatii_readable)

                results_text = f"Directorul General Administrativ în ASE poate fi demis de {de} în următoarele situații: {situatii_text}."


            elif identified_entity == "RESPONSABILITATI_GESTIONARE_ECONOMICO_FINANCIARA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Directorul General Administrativ are responsabilități semnificative în gestionarea economico-financiară în ASE."


            elif identified_entity == "CONDUCERE_OPERATIVA_DEPARTAMENT":
                val = results["results"]["bindings"][0]['value']['value']
                if val == 'true':
                    results_text = "Directorul de Departament are responsabilități semnificative în asigurarea conducerii operaționale, coordonând activitățile zilnice și luând decizii importante la nivelul departamentului."
                else:
                    results_text = "Directorul de Departament nu asigură în mod direct conducerea operațională a departamentului, sau responsabilitățile sale în această zonă sunt minime."

            elif identified_entity == "REVOCARE_DIRECTOR_DEPARTAMENT":
                revocare_initiator = results["results"]["bindings"][0].get('de', {}).get('value', 'N/A')

                # Defining the properties related for Directorul de Departament
                situatii_props = [
                    "cerereMajoritatePersonal",
                    "incalcareCodEticaDeontologie",
                    "incalcareIndatoriri",
                    "incompatibilitateLegal",
                    "prejudiciuInteresePrestigiuASE"
                ]
                situatii_readable = [format_property_name(prop) for prop in situatii_props]
                situatii_text = ", ".join(situatii_readable)
                results_text = f"Directorul de Departament poate fi revocat de {revocare_initiator} în următoarele situații: {situatii_text}."

            elif identified_entity == "SARCINI_DIRECTOR_DEPARTAMENT":
                sarcini_list = []

                for result in results["results"]["bindings"]:
                    for sarcina in ["avizeazaCereriAnSabatic", "contribuiePlanuriDeInvatamant", "coordoneazaCercetare",
                                    "elaboreazaStateDeFunctii", "imbunatatesteEducatieCercetare",
                                    "indeplinesteSarciniFisaPostului", "intocmesteFiseDePost",
                                    "organizeazaSelectieEvaluarePersonal", "propuneNormeDidactice",
                                    "propunePosturiDidactice", "raspundeManagementCalitateFinanciar",
                                    "raspundeOrganizareConcursuri"]:

                        if sarcina in result and result[sarcina]['value'] == "true":
                            formatted_sarcina = format_property_name(sarcina)
                            sarcini_list.append(formatted_sarcina)

                if sarcini_list:
                    sarcini_text = ", ".join(sarcini_list)
                    results_text = f"Sarcinile Directorului de Departament în ASE includ: {sarcini_text}."

                else:
                    results_text = "Nu s-au găsit detalii specifice despre sarcinile Directorului de Departament."


            elif identified_entity == "SELECTIE_DIRECTOR_DEPARTAMENT":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Directorul de Departament în ASE este selectat prin {val}."

            elif identified_entity == "CONDUCERE_OPERATIVA_SCOLI_DOCTORALE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Directorul Școlii Doctorale asigură conducerea operativă în ASE." if val == "true" else "Directorul Școlii Doctorale nu asigură conducerea operativă în ASE."

            elif identified_entity == "REVOCARE_DIRECTOR_SCOLI_DOCTORALE":
                revocare_reasons = []
                revocare_initiator = None

                for result in results["results"]["bindings"]:
                    if 'de' in result:
                        revocare_initiator = result['de']['value']
                    for situatie in ["cerereMajoritateSimpleConducatoriDoctorat", "incalcareCodEticaDeontologie",
                                     "incalcareIndatoririStandardePerformanta", "incompatibilitateLegal",
                                     "prejudiciuInteresePrestigiuASE"]:
                        if situatie in result and result[situatie]['value'] == "true":
                            formatted_situatie = format_property_name(situatie)
                            revocare_reasons.append(formatted_situatie)

                if revocare_reasons:
                    reasons_text = "; ".join(revocare_reasons)
                    initiator_text = f" de {revocare_initiator}" if revocare_initiator else ""
                    results_text = f"Directorul Școlii Doctorale în ASE poate fi revocat{initiator_text} în următoarele situații: {reasons_text}."
                else:
                    results_text = "Nu s-au găsit detalii specifice despre situațiile de revocare a Directorului Școlii Doctorale."

            elif identified_entity == "SARCINI_DIRECTOR_SCOLI_DOCTORALE":
                sarcini_list = []

                for result in results["results"]["bindings"]:
                    for sarcina in entity_mapping[identified_entity]["node_properties"]:
                        if sarcina in result and result[sarcina]['value'] == "true":
                            formatted_sarcina = format_property_name(sarcina)
                            sarcini_list.append(formatted_sarcina)

                if sarcini_list:
                    sarcini_text = "; ".join(sarcini_list)
                    results_text = f"Sarcinile Directorului Școlii Doctorale în ASE includ: {sarcini_text}."
                else:
                    results_text = "Nu s-au găsit detalii specifice despre sarcinile Directorului Școlii Doctorale."

            elif identified_entity == "SELECTIE_DIRECTOR_SCOLI_DOCTORALE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Directorul Școlii Doctorale în ASE este selectat {val}."

            elif identified_entity == "DREPTURI_PERSONAL_DIDACTIC_CERCETARE":
                drepturi_list = []

                for result in results["results"]["bindings"]:
                    for drept in entity_mapping[identified_entity]["node_properties"]:
                        if drept in result and result[drept]['value'] == "true":
                            formatted_drept = format_property_name(drept)
                            drepturi_list.append(formatted_drept)

                if drepturi_list:
                    drepturi_text = ", ".join(drepturi_list)
                    results_text = f"Personalul didactic și de cercetare în ASE are următoarele drepturi: {drepturi_text}."
                else:
                    results_text = "Nu s-au găsit detalii specifice despre drepturile personalului didactic și de cercetare în ASE."

            elif identified_entity == "OBLIGATII_PERSONAL_DIDACTIC_CERCETARE":
                obligatii_list = []

                for result in results["results"]["bindings"]:
                    for obligatie in entity_mapping[identified_entity]["node_properties"]:
                        if obligatie in result and result[obligatie]['value'] == "true":
                            formatted_obligatie = format_property_name(obligatie)
                            obligatii_list.append(formatted_obligatie)

                if obligatii_list:
                    obligatii_text = ", ".join(obligatii_list)
                    results_text = f"Personalul didactic și de cercetare în ASE are următoarele obligații: {obligatii_text}."
                else:
                    results_text = "Nu s-au găsit detalii specifice despre obligațiile personalului didactic și de cercetare în ASE."

            elif identified_entity == "EXPRIMARE_LIBERA_OPINII":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Exprimarea liberă a opiniilor este permisă pentru personalul didactic și de cercetare în ASE." if val == "true" else "Nu există informații specifice despre permisiunea exprimării libere a opiniilor pentru personalul didactic și de cercetare în ASE."

            elif identified_entity == "MOBILITATE_INTERNATIONALA":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Mobilitatea internațională este reglementată și încurajată pentru personalul didactic și de cercetare în ASE." if val == "true" else "Nu există informații specifice despre reglementarea mobilității internaționale pentru personalul didactic și de cercetare în ASE."

            elif identified_entity == "CONCEDIILE_CU_FARA_PLATA":
                concedii_cu_plata = any(
                    result['concediiCuPlata']['value'] == "true" for result in results["results"]["bindings"] if
                    'concediiCuPlata' in result)
                concedii_fara_plata = any(
                    result['concediiFaraPlata']['value'] == "true" for result in results["results"]["bindings"] if
                    'concediiFaraPlata' in result)
                results_text = "Concediile cu plată " + (
                    "sunt permise" if concedii_cu_plata else "nu sunt permise") + " și concediile fără plată " + ("sunt permise" if concedii_fara_plata else "nu sunt permise") + " pentru personalul didactic și de cercetare în ASE."

            elif identified_entity == "PROTECTIE_SPATIU_UNIVERSITAR":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = "Spațiul universitar este protejat pentru personalul didactic și de cercetare în ASE, prin asigurarea unor condiții de lucru sigure și echitabile, implementarea de politici împotriva discriminării și hărțuirii, promovarea unui climat de respect reciproc și susținerea libertății academice și a drepturilor profesionale." if val == "true" else "Nu există informații specifice despre protecția spațiului universitar pentru personalul didactic și de cercetare în ASE."

            elif identified_entity == "EVALUARE_PERIODICA":
                val = results["results"]["bindings"][0]['evaluarePeriodica']['value']
                results_text = "Evaluarea periodică a personalului didactic și de cercetare este o practică în ASE, prin care se monitorizează și îmbunătățește calitatea predării și activităților de cercetare, asigurând excelența educațională și promovarea valorilor academice." if val == "true" else "Nu există informații specifice despre evaluarea periodică a personalului didactic și de cercetare în ASE."

            elif identified_entity == "CONTRIBUIRE_MISIUNE_ASE":
                val = results["results"]["bindings"][0]['contribuireMisiuneASE']['value']
                results_text = "Personalul didactic și de cercetare contribuie semnificativ la misiunea ASE, prin implicarea activă în activități de cercetare, inovare și dezvoltare academică, asigurând astfel excelența educațională și promovarea valorilor academice." if val == "true" else "Nu există informații specifice despre contribuția personalului didactic și de cercetare la misiunea ASE."

            elif identified_entity == "ACCES_HOTARARI":
                val = result['value']['value']
                results_text = f"Studenții ASE au dreptul la accesul la hotărârile structurilor de conducere, precum {val}."

            elif identified_entity == "BENEFICIERE_ASISTENTA_MEDICALA":
                val = result['value']['value']
                results_text = f"Studenții ASE pot beneficia de asistență medicală și psihologică gratuită {val}."

            elif identified_entity == "BENEFICIERE_CAZARE":
                val = result['value']['value']
                results_text = f"Dreptul la cazare pentru studenții ASE este asigurat {val}."

            elif identified_entity == "BENEFICIERE_PROTECTIE_UNIVERSITAR":
                val = result['value']['value']
                results_text = f"Protecția spațiului universitar pentru studenții ASE este asigurată {val}."

            elif identified_entity == "BENEFICIERE_SERVICII":
                val = result['value']['value']
                results_text = f"Studenții ASE au acces la facilități și servicii, inclusiv {val}."

            elif identified_entity == "CONTESTARE_NOTE":
                val = result['value']['value']
                results_text = f"Studenții ASE pot contesta notele obținute conform {val}."

            elif identified_entity == "PROPRIETATE_INTELECTUALA":
                val = result['value']['value']
                results_text = f"Studenții ASE au drepturi legate de proprietatea intelectuală, inclusiv {val}."

            elif identified_entity == "DESFASURARE_ACTIUNI":
                val = result['value']['value']
                results_text = f"Participarea studenților ASE la activități extracurriculare este reglementată prin {val}."

            elif identified_entity == "LIMITARE_ORAR":
                val = result['value']['value']
                results_text = f"Orarul studenților ASE este unul {val}."

            elif identified_entity == "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE":
                val = result['value']['value']
                results_text = f"Studenții ASE pot participa la procesul de elaborare a regulamentelor universitare prin: {val}."

            elif identified_entity == "RECUNOASTERE_PRACTICA_INDIVIDUALA":
                val = result['value']['value']
                results_text = f"Practica individuală a studenților ASE este recunoscută prin: {val}."

            elif identified_entity == "PROTECTIE_DATE_PERSONALE":
                val = result['value']['value']
                results_text = f"Protecția datelor personale ale studenților ASE este asigurată conform: {val}."

            elif identified_entity == "STUDIU_LIMBA_INTERNATIONALA":
                val = result['value']['value']
                results_text = f"Studenții ASE pot studia într-o limbă internațională în condițiile: {val}."

            elif identified_entity == "SESIZARE_ABUZURI":
                val = result['value']['value']
                results_text = f"Studenții ASE pot sesiza abuzuri {val}."

            elif identified_entity == "TERMENE_INSCRIERE":
                val = result['value']['value']
                results_text = f"Termenele pentru înscrierea la activitățile universitare în ASE sunt stabilite {val}."

            elif identified_entity == "UTILIZARE_FACILITATI":
                val = result['value']['value']
                results_text = f"Studenții ASE pot utiliza facilitățile universității {val}."

            elif identified_entity == "STUDII_GRATUITE_CENTRE_PLASAMENT":
                val = result['value']['value']
                results_text = f"Studenții absolvenți din centrele de plasament beneficiază de {val} la ASE."

            elif identified_entity == "ACCES_ADAPTAT_DIZABILITATI":
                val = result['value']['value']
                results_text = f"ASE asigură acces adaptat pentru studenții cu dizabilități, inclusiv {val}."

            elif identified_entity == "CONDITII_NORMALE_DIZABILITATI":
                val = result['value']['value']
                results_text = f"ASE creează condiții normale pentru studenții cu dizabilități, prin {val}."

            elif identified_entity == "BENEFICIERE_LOGISTICA_DOCTORAT":
                val = result['value']['value']
                results_text = f"Studenții doctoranzi au acces la resurse logistice, cum ar fi {val}."

            elif identified_entity == "COLABORARE_ECHIPE_CERCETARE":
                val = result['value']['value']
                results_text = f"Studenții doctoranzi ASE pot colabora cu echipe de cercetare, beneficiind de {val}."

            elif identified_entity == "MOBILITATI_DOCTORAT":
                val = result['value']['value']
                results_text = f"Studenții doctoranzi la ASE au acces la mobilități, inclusiv {val}."

            elif identified_entity == "REPREZENTARE_FORURI_DOCTORAT":
                val = result['value']['value']
                results_text = f"Studenții doctoranzi sunt reprezentați în forurile decizionale ASE, având {val}."

            elif identified_entity == "GRATUITATE_MANIFESTARI_ROMANI":
                val = result['value']['value']
                results_text = f"Studenții etnici români beneficiază de gratuitate la manifestări, prin {val}."

            elif identified_entity == "LOCURI_FINANTATE_MARGINALIZATI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Locurile finanțate alocate pentru candidații din medii marginalizate în ASE sunt: {val}."

            elif identified_entity == "SERVICII_URMARIRE_MARGINALIZATI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Serviciile de urmărire oferite studenților marginalizați pentru integrarea în ASE sunt: {val}."

            elif identified_entity == "EVIDENTA_STUDENTI":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Evidența studenților în cadrul facultăților ASE este ținută de: {val}."

            elif identified_entity == "DEFINITIE_FACULTATE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Facultatea în structura ASE reprezintă: {val}."

            elif identified_entity == "ORGANISM_DECIZIONAL_FACULTATE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Organismul decizional al unei facultăți în ASE este {val}."


            elif identified_entity == "STRUCTURA_FACULTATE":
                structura_set = set()

                for result in results["results"]["bindings"]:
                    for prop in ["departamente", "extensiiUniversitare", "școliDoctorale", "școliPostuniversitare"]:
                            if prop in result:
                                structura_set.add(format_property_name(prop))

                # Converting the set to a sorted list
                structura = ', '.join(sorted(structura_set))

                results_text = f"Structura facultății în ASE include: {structura}."

            elif identified_entity == "INFIINTARE_FUNCTIONARE_DESFIINTARE_FACULTATE":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Facultățile în ASE se înființează, funcționează și se desființează {val}."


            elif identified_entity == "CONTRACTE_MINISTER_RESORT":
                val = results["results"]["bindings"][0]['value']['value']

                if val == 'true':
                    results_text = "ASE este finanțată prin contracte cu Ministerul de resort, implicând finanțare directă pentru diverse proiecte și inițiative academice."
                else:
                    results_text = "ASE nu este finanțată prin contracte cu Ministerul de resort sau aceste contracte nu constituie o sursă semnificativă de finanțare."

            elif identified_entity == "FINANTARE_ALTE_SURSE":
                val = results["results"]["bindings"][0]['value']['value']

                if val == 'true':
                    results_text = "Sursele alternative de finanțare pentru ASE includ diverse metode, cum ar fi finanțări de la alte ministere, împrumuturi sau surse externe."
                else:
                    results_text = "Nu există surse alternative de finanțare specificate pentru ASE."


            elif identified_entity == "FINANTARE_CERCETARE_STIINTIFICA":
                val = results["results"]["bindings"][0]['value']['value']

                if val == 'true':
                    results_text = "Cercetarea științifică în ASE este finanțată prin diverse surse, inclusiv granturi guvernamentale și parteneriate private."
                else:
                    results_text = "Nu există finanțare specificată pentru cercetarea științifică în ASE."


            elif identified_entity == "FINANTARE_TAXE_SCOLARIZARE":
                val = results["results"]["bindings"][0]['value']['value']

                if val == 'true':
                    results_text = "Taxele de școlarizare și prestațiile universitare joacă un rol semnificativ în finanțarea ASE, susținând diverse activități academice și infrastructura."
                else:
                    results_text = "Rolul taxelor de școlarizare și prestațiilor universitare în finanțarea ASE nu este semnificativ, sau acestea nu contribuie în mod direct la bugetul principal."


            elif identified_entity == "VENITURI_PROPRII":
                val = results["results"]["bindings"][0]['value']['value']

                if val == 'true':
                    results_text = "Contribuția veniturilor proprii la bugetul ASE este semnificativă, implicând diverse surse de venit autonom, cum ar fi taxe de școlarizare, servicii academice și partenere comerciale."
                else:
                    results_text = "Contribuția veniturilor proprii la bugetul ASE nu este semnificativă sau nu există în prezent."

            elif identified_entity == "CONFLICT_INTERESE_SITUATII":
                situatii = []
                for result in results["results"]["bindings"]:
                    for prop in entity_mapping["CONFLICT_INTERESE_SITUATII"]["node_properties"]:
                        if prop in result:
                            situatii.append(format_property_name(prop))
                results_text = "Situațiile care pot genera un conflict de interese în ASE includ: " + ', '.join(situatii) + "."

            elif identified_entity == "INFORMARE_CONFLICT":
                informare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Informarea despre existența unui conflict de interese în ASE se face {informare}."

            elif identified_entity == "REZOLVARE_INCOMPATIBILITATE":
                termen = results["results"]["bindings"][0]['value']['value']
                results_text = f"Rezolvarea unei situații de incompatibilitate se face {termen}."

            elif identified_entity == "MANIFESTARE_LIBERTATE_ACADEMICA":
                manifestari = []
                for result in results["results"]["bindings"]:
                    for prop in entity_mapping["MANIFESTARE_LIBERTATE_ACADEMICA"]["node_properties"]:
                        # Checking if the property exists
                        if prop in result and result[prop]['type'] == 'literal' and result[prop]['value'] != "true":
                            manifestari.append(format_property_name(prop) + ": " + result[prop]['value'])

                if manifestari:
                    results_text = "Libertatea academică în ASE se manifestă prin: " + ', '.join(manifestari) + "."
                else:
                    results_text = "Nu s-au găsit detalii despre manifestările libertății academice în ASE."

            elif identified_entity == "PERMISE_ACTIVITATI":
                activitati = results["results"]["bindings"][0]['value']['value']
                results_text = f"Activitățile permise în ASE conform libertății academice sunt: {activitati}."


            elif identified_entity == "PRINCIPII_MANAGEMENT_CALITATE":
                principii = []
                for result in results["results"]["bindings"]:
                    prop = result['property']['value'].split('#')[-1]
                    value = result.get('value', {}).get('value','').lower()

                    if prop == 'type' or value not in ['true', 'false']:
                        continue

                    formatted_prop = format_property_name(prop)
                    principii.append(formatted_prop)

                if principii:
                    results_text = "Principiile managementului calității universitare în ASE includ: " + '; '.join(principii) + "."
                else:
                    results_text = "Nu s-au găsit principii specifice ale managementului calității universitare în ASE."

            elif identified_entity == "EVALUARE_ACTIVITATE_DIDACTICA_STIINTIFICA":
                evaluare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Evaluarea activității didactice și științifice în ASE se realizează: {evaluare}."

            elif identified_entity == "PROCEDURI_EVALUARE_CALITATE":
                proceduri = results["results"]["bindings"][0]['value']['value']
                results_text = f"Procedurile de evaluare a calității în ASE sunt: {proceduri}."

            elif identified_entity == "STUDENTI_IMPLICARE_MANAGEMENT":
                implicare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Implicarea studenților în managementul ASE se face {implicare}."

            elif identified_entity == "MISIUNE_CERCETARE":
                misiune_cercetare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Misiunea de cercetare a ASE: {misiune_cercetare}"

            elif identified_entity == "MISIUNE_EDUCATIONALA":
                misiune_educationala = results["results"]["bindings"][0]['value']['value']
                results_text = f"Misiunea educațională a ASE: {misiune_educationala}."

            elif identified_entity == "MISIUNE_COMUNITATE":
                misiune_comunitate = results["results"]["bindings"][0]['value']['value']
                results_text = f"Misiunea Comunitara ASE este {misiune_comunitate}"

            elif identified_entity == "OBLIGATII_FINANCIARE_STUDENTI":
                obligatii_financiare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Obligațiile ale studenților față de ASE sunt {obligatii_financiare}."

            elif identified_entity == "COMPORTAMENT_CIVIC":
                comportament_civic = results["results"]["bindings"][0]['value']['value']
                results_text = f"Studenții ASE trebuie să manifeste un comportament civic {comportament_civic}."

            elif identified_entity == "RESPECTARE_CURATENIE_ORDINE":
                curatenie_ordine = results["results"]["bindings"][0]['value']['value']
                results_text = f"Studenții ASE trebuie să respecte {curatenie_ordine}."

            elif identified_entity == "RESPECTARE_STANDARDE_CALITATE":
                standarde_calitate = results["results"]["bindings"][0]['value']['value']
                results_text = f"Studenții ASE trebuie să respecte standardele {standarde_calitate}, cum ar fi participarea activă la cursuri și seminarii, realizarea la timp a proiectelor și temelor, menținerea unui comportament etic și responsabil, și implicarea în activități extracurriculare și de voluntariat.."

            elif identified_entity == "UTILIZARE_FACILITATI":
                utilizare_facilitati = results["results"]["bindings"][0]['utilizareFacilitati']['value']
                results_text = f"Studenții ASE pot utiliza facilitățile universitare în mod corespunzător: {utilizare_facilitati}."

            elif identified_entity == "OBLIGATIE_CONDUCATOR_DOCTORAT":
                obligatie_cond_doctorat = results["results"]["bindings"][0]['fieLegaturaPermanenta']['value']
                results_text = f"Obligația studenților doctoranzi față de conducătorul de doctorat: {obligatie_cond_doctorat}."

            elif identified_entity == "PREZENTARE_RAPOARTE":
                prezentare_rapoarte = results["results"]["bindings"][0]['prezentareRapoarte']['value']
                results_text = f"Studenții doctoranzi trebuie să prezinte rapoarte de activitate: {prezentare_rapoarte}."

            elif identified_entity == "RESPECTARE_DISCIPLINA":
                respectare_disciplina = results["results"]["bindings"][0]['respectareDisciplina']['value']
                results_text = f"Studenții doctoranzi trebuie să respecte disciplina instituțională: {respectare_disciplina}."

            elif identified_entity == "RESPECTARE_PROGRAM_PREGATIRE":
                respectare_program_pregatire = results["results"]["bindings"][0]['respectareProgramPregatire']['value']
                results_text = f"Programul de pregătire pe care studenții doctoranzi trebuie să-l respecte: {respectare_program_pregatire}."

            elif identified_entity == "GESTIONARE_PATRIMONIU":
                aprobare = results["results"]["bindings"][0]['aprobareCuantumStructuraAport']['value']
                results_text = f"Patrimoniul ASE este gestionat și structura și cuantumul contribuțiilor sunt aprobate de {aprobare}."

            elif identified_entity == "INCHIRIERE_ACTIVE_PATRIMONIALE":
                inchiriere = "permisă" if results["results"]["bindings"][0]['inchiriereActivePatrimoniale'][
                                              'value'] == "true" else "nepermisă"
                results_text = f"ASE poate închiria active patrimoniale: {inchiriere}."

            elif identified_entity == "PARTICIPARE_FUNDATII_ASOCIATII":
                participare = results["results"]["bindings"][0]['participareFundatiiAsociatiiSocietatiComerciale'][
                    'value']
                results_text = f"Participarea ASE la fundații, asociații și societăți comerciale este aprobată de {participare}."

            elif identified_entity == "TITULAR_DREPT_ADMINISTRARE":
                titular = "este" if results["results"]["bindings"][0]['titularaDreptAdministrareBunuriStat'][
                                        'value'] == "true" else "nu este"
                results_text = f"ASE {titular} titularul dreptului de administrare a bunurilor statului."

            elif identified_entity == "PRINCIPII_COD_ETICA":
                principii = results["results"]["bindings"][0]['value']['value']
                results_text = f"Principiile Codului de Etică în ASE includ atitudinea {principii}"

            elif identified_entity == "COMPORTAMENT_FATA_STUDENTI":
                comportament = results["results"]["bindings"][0]['conduita']['value']
                results_text = f"Conduita morală adecvată în raport cu studenții este: {comportament}."

            elif identified_entity == "COOPERARE_COMUNITARA":
                cooperare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Cooperarea comunitară și atitudinea neconflictuală sunt subliniate în codul etic al ASE ca {cooperare}."

            elif identified_entity == "COMPONENTA_COMISIE_ETICA":
                componența = results["results"]["bindings"][0]['compozitie']['value']
                results_text = f"Componența Comisiei de Etică și Deontologie Universitară în ASE este determinată prin {componența}."

            elif identified_entity == "PRINCIPII_CONDUITA":
                principii_conduita = []

                for result in results["results"]["bindings"]:
                        for prop in ["conduitaMoralaAdecvata", "evitareHartuire", "masuriAnticipativeSuprasolicitare",
                                 "solutionareNemultumiriCaleIerarhica"]:

                             if result[prop]['value'] == "true":
                                principii_conduita.append(format_property_name(prop))

                results_text = "Principiile de conduită stabilite în ghidurile etice ale ASE includ: " + ', '.join(principii_conduita) + "."

            elif identified_entity == "CRITERII_EXCLUDERE":
                exclusi = results["results"]["bindings"][0]['excludere']['value']
                results_text = f"Din Comisia de Etică și Deontologie Universitară în ASE sunt excluse {exclusi}."


            elif identified_entity == "NUMIRE_PRODECAN":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Prodecanul în ASE este numit de {val}."

            elif identified_entity == "DEMITERE_PRODECAN":
                de = results["results"]["bindings"][0].get('de', {}).get('value', 'N/A')
                results_text = f"Prodecanul poate fi demis de {de}."

            elif identified_entity == "SITUATII_DEMITERE_PRODECAN":

                de = results["results"]["bindings"][0].get('de', {}).get('value', 'N/A')

                situatii_props = ["incalcareCodEticaDeontologie", "incalcareLegislatieNormeEtica",
                                  "incompatibilitateLegal", "neindeplinireSarcini", "prejudiciuInteresePrestigiuASE"]

                situatii_readable = [format_property_name(prop) for prop in situatii_props]
                situatii_text = ", ".join(situatii_readable)

                results_text = f"Prodecanul poate fi demis de {de}. Situațiile care pot duce la demitere includ: {situatii_text}."


            elif identified_entity == "SARCINI_STABILITE_PRODECAN":
                val = results["results"]["bindings"][0]['value']['value']
                results_text = f"Sarcinile Prodecanului sunt stabilite de {val}."

            elif identified_entity == "ADMITERE_PROGRAME_STUDII":
                conditii_cetateni = 'N/A'
                conformitate_legislatie = 'neconforme cu legislația'
                metodologii_proprii = 'fără a folosi metodologii proprii'

                for binding in results["results"]["bindings"]:
                    if 'condițiiCetățeni' in binding:
                        conditii_cetateni = binding['condițiiCetățeni']['value']
                    if 'conformitateLegislație' in binding and binding['conformitateLegislație']['value'] == "true":
                        conformitate_legislatie = "conforme cu legislația"
                    if 'metodologiiProprii' in binding and binding['metodologiiProprii']['value'] == "true":
                        metodologii_proprii = "folosind metodologii proprii"

                results_text = f"Admiterea în programele de studii ASE pentru cetățenii UE și non-UE se realizează {conditii_cetateni}, {conformitate_legislatie} și {metodologii_proprii}."

            elif identified_entity == "CALIFICARI_DOCUMENTE":
                atestare = 'N/A'
                echivalenta = 'N/A'
                organizare_comuna = 'N/A'

                for binding in results["results"]["bindings"]:
                    if 'atestare' in binding:
                        atestare = binding['atestare']['value']
                    if 'echivalență' in binding:
                        echivalenta = binding['echivalență']['value']
                    if 'organizareComună' in binding:
                        organizare_comuna = binding['organizareComună']['value']

                results_text = f"Calificările obținute de studenții ASE sunt validate prin {atestare}, echivalența {echivalenta} și sunt organizate în comună conform {organizare_comuna}."

            elif identified_entity == "ALOCARE_CREDITE":

                alocare_conform = 'N/A'

                element_referinta = 'N/A'

                numar_specific = 'N/A'

                precizare_plan_invatamant = 'N/A'

                regulamente = 'N/A'

                volum_munca_intelectuala = 'N/A'

                scoli_vara_si_voluntariat = 'N/A'

                # Iterating through each binding in the results

                for binding in results["results"]["bindings"]:

                    if 'alocareConform' in binding:
                        alocare_conform = binding['alocareConform']['value']

                    if 'elementReferință' in binding:
                        element_referinta = binding['elementReferință']['value']

                    if 'numărSpecific' in binding:
                        numar_specific = "da" if binding['numărSpecific']['value'] == "true" else "nu"

                    if 'precizarePlanÎnvățământ' in binding:
                        precizare_plan_invatamant = "da" if binding['precizarePlanÎnvățământ']['value'] == "true" else "nu"

                    if 'regulamente' in binding:
                        regulamente = binding['regulamente']['value']

                    if 'volumMuncăIntelectuală' in binding:
                        volum_munca_intelectuala = binding['volumMuncăIntelectuală']['value']

                    if 'școliVarăȘiVoluntariat' in binding:
                        scoli_vara_si_voluntariat = binding['școliVarăȘiVoluntariat']['value']

                results_text = f"Creditele în programele de studii ASE sunt alocate conform {alocare_conform}, cu referință la {element_referinta}. Numărul de credite este specific: {numar_specific}, iar planul de învățământ este precizat: {precizare_plan_invatamant}. Regulamentele sunt {regulamente}. Volumul de muncă intelectuală implică {volum_munca_intelectuala}, iar școlile de vară și voluntariatul sunt considerate: {scoli_vara_si_voluntariat}."


            elif identified_entity == "FORME_ORGANIZARE_STUDII":

                cu_frecventa = 'N/A'

                cu_frecventa_redusa = 'N/A'

                la_distanta = 'N/A'

                for binding in results["results"]["bindings"]:

                    if 'cuFrecvență' in binding:
                        cu_frecventa = binding['cuFrecvență']['value']

                    if 'cuFrecvențăRedusă' in binding:
                        cu_frecventa_redusa = binding['cuFrecvențăRedusă']['value']

                    if 'laDistanță' in binding:
                        la_distanta = binding['laDistanță']['value']

                results_text = f"Formele de organizare a studiilor disponibile în ASE includ studiile cu frecvență: {cu_frecventa}, cu frecvență redusă: {cu_frecventa_redusa} și la distanță: {la_distanta}."

            elif identified_entity == "STRUCTURA_AN_UNIVERSITAR":
                aprobare = results["results"]["bindings"][0].get('aprobare', {}).get('value', 'N/A')
                conformitate = "conform prevederilor legale în vigoare" if \
                    results["results"]["bindings"][1]['conformitate'][
                        'value'] == "true" else "neconform prevederilor legale în vigoare"
                results_text = f"Structura anilor universitari în cadrul programelor de studii ASE este aprobată de {aprobare} și este {conformitate}."


            elif identified_entity == "TIPURI_PROGRAME_STUDII":
                studii_formare_profesionala = results["results"]["bindings"][0].get('studiileFormareProfesionalăAdult',{}).get('value', 'N/A')
                studii_postuniversitare = "sunt oferite" if results["results"]["bindings"][0].get('studiilePostuniversitare', {}).get('value', 'false') == "true" else "nu sunt oferite"

                if len(results["results"]["bindings"]) > 1:
                    studii_universitare = results["results"]["bindings"][1].get('studiileUniversitare', {}).get('value','N/A')

                else:
                    studii_universitare = 'N/A'

                results_text = f"Tipurile de programe de studii oferite de ASE includ studiile de formare profesională pentru adulți {studii_formare_profesionala}, studiile postuniversitare {studii_postuniversitare} și studiile universitare {studii_universitare}."

            elif identified_entity == "DURATA_MANDAT":
                durata = results["results"]["bindings"][0]['value']['value']
                results_text = f"Durata mandatului pentru un Prorector în ASE este de {durata}."


            elif identified_entity == "CONDITII_DEMITERE_PRORECTOR":

                de = results["results"]["bindings"][0].get('de', {}).get('value', 'N/A')

                motive_details = set()

                for result in results["results"]["bindings"]:

                    if result.get('incalcareLegislatieNormeEtica', {}).get('value') == 'true':
                        motive_details.add("încălcarea legislației și normelor etice")

                    if result.get('incompatibilitateLegala', {}).get('value') == 'true':
                        motive_details.add("incompatibilitate legală")

                    if result.get('nendeplinireSarcini', {}).get('value') == 'true':
                        motive_details.add("nendeplinirea sarcinilor")

                    if result.get('prejudiciuIntereseASE', {}).get('value') == 'true':
                        motive_details.add("prejudiciul intereselor ASE")

                # Converting the set of motives to a sorted list and join them into a text string

                motive_text = ', '.join(sorted(motive_details))
                results_text = f"Un Prorector în ASE poate fi demis de {de} din motive precum: {motive_text}."

            elif identified_entity == "SARCINI_PRORECTOR":
                sarcini_text = []

                for result in results["results"]["bindings"]:
                    for task_name, task_detail in result.items():
                        if task_detail['value'].lower() == 'true':
                            formatted_name = format_property_name(task_name)
                            sarcini_text.append(formatted_name)

                results_text = "Sarcinile Prorectorului în ASE includ: " + ', '.join(sarcini_text) + "."

            elif identified_entity == "ASIGURARE_CALITATE":
                asigurareCalitate = result['asigurareCalitate']['value'] == 'true'

                if asigurareCalitate:
                    results_text = "Prorectorul contribuie la asigurarea calității în ASE prin supravegherea și îmbunătățirea continuă a standardelor academice."

                else:
                    results_text = "Nu s-a putut găsi informații despre contribuția prorectorului la asigurarea calității în ASE."

            elif identified_entity == "ATRAGERE_FONDURI_EUROPENE":
                atragereFonduriEuropene = result['atragereFonduriEuropene']['value'] == 'true'

                if atragereFonduriEuropene:
                    results_text = "Prorectorul joacă un rol crucial în atragerea de fonduri europene pentru ASE, coordonând propunerile de proiecte și stabilind parteneriate strategice."

                else:
                    results_text = "Nu s-a putut găsi informații despre contribuția prorectorului la atragerea de fonduri europene în ASE."


            elif identified_entity == "ORGANIZARE_PROGRAM_STUDII":
                organizareProgramStudii = result['organizareProgramStudii']['value'] == 'true'

                if organizareProgramStudii:
                    results_text = "Prorectorul este implicat activ în organizarea programelor de studii în ASE, asigurându-se că acestea răspund nevoilor educaționale actuale."

                else:
                    results_text = "Nu s-a putut găsi informații despre implicarea prorectorului în organizarea programelor de studii în ASE."


            elif identified_entity == "RELAȚII_INTERNAȚIONALE":
                relatiiInternationale = result['relatiiInternationale']['value'] == 'true'

                if relatiiInternationale:
                    results_text = "Prorectorul are responsabilități semnificative în ceea ce privește relațiile internaționale ale ASE, promovând colaborări și parteneriate cu instituții de învățământ superior din întreaga lume."
                else:
                    results_text = "Nu s-a putut găsi informații despre implicarea prorectorului în relațiile internaționale ale ASE."

            elif identified_entity == "ATRIBUTII_RECTOR":
                atributii = []

                for result in results["results"]["bindings"]:
                    for prop, prop_info in result.items():
                        if prop_info['value'] == 'true':
                            formatted_prop_name = format_property_name(prop)
                            atributii.append(formatted_prop_name)

                atributii_text = ', '.join(atributii)
                results_text = f"Atribuțiile Rectorului în ASE includ: {atributii_text}."

            elif identified_entity == "DESEMNARE_RECTOR":
                desemnare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Rectorul în ASE este desemnat prin {desemnare}."

            elif identified_entity == "DURATA_MANDAT_RECTOR":
                durata = 'N/A'
                max_mandate = 'N/A'

                for binding in results["results"]["bindings"]:
                    prop = binding['property']['value'].split('#')[-1]
                    value = binding['value']['value']

                    if prop == 'mandat':
                        durata = value
                    elif prop == 'maxMandate':
                        max_mandate = value
                results_text = f"Durata mandatului Rectorului în ASE este de {durata} și poate avea maxim {max_mandate} mandate."

            elif identified_entity == "CONDITII_DEMITERE_RECTOR":
                result = results["results"]["bindings"][0]
                de = result['de']['value']

                # Dictionary to hold the SPARQL variables and their human-readable names

                situatii = {
                    'Încălcarea legislației și normelor de etică': result['incalcareLegislatieNormeEtica']['value'] == 'true',
                    'Incompatibilitate legală': result['incompatibilitateLegala']['value'] == 'true',
                    'Neîndeplinirea indicatorilor': result['neindeplinireIndicatori']['value'] == 'true',
                    'Prejudiciu adus intereselor și prestigiului ASE': result['prejudiciuInteresePrestigiuASE']['value'] == 'true'
                }

                valid_situations = [format_property_name(description) for description, valid in situatii.items() if valid]
                situatii_text = ', '.join(valid_situations)

                results_text = f"Rectorul poate fi demis sau revocat de {de} în următoarele situații: {situatii_text}."

            elif identified_entity == "CONTRIBUIE_CONDUCERE_OPERATIONALA":
                contributie = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"
                if contributie == "true":
                    results_text = "Rectorul contribuie semnificativ la conducerea operațională a ASE prin gestionarea eficientă a resurselor și coordonarea activităților academice și administrative."
                else:
                    results_text = "Rectorul nu are contribuții semnificative la conducerea operațională a ASE conform datelor disponibile."

            elif identified_entity == "ASIGURARE_BUNA_DESFASURARE_CONCURSURI":
                asigurare = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"
                if asigurare == "true":
                    results_text = "Rectorul asigură buna desfășurare a concursurilor în ASE, garantând transparența și echitatea procesului de selecție."
                else:
                    results_text = "Rectorul nu asigură în mod explicit buna desfășurare a concursurilor în ASE conform datelor disponibile."

            elif identified_entity == "ROL_GESTIONARE_PATRIMONIU":
                rol = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"
                if rol == "true":
                    results_text = "Rectorul are un rol crucial în gestionarea patrimoniului ASE, supraveghind utilizarea responsabilă și dezvoltarea infrastructurii universitare."
                else:
                    results_text = "Rectorul nu are un rol activ în gestionarea patrimoniului ASE conform datelor disponibile."

            elif identified_entity == "ROL_MEMBRU_FONDATOR_USASE":
                rol = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE, ca membru fondator {rol}, joacă un rol esențial în dezvoltarea și susținerea inițiativelor studențești."

            elif identified_entity == "PARTICIPARE_ORGANIZARE_ALEGERI":
                participare = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE participă activ la organizarea alegerilor pentru structurile de conducere academică {participare}."

            elif identified_entity == "REPREZENTARE_INTERESE_STUDENTI":
                reprezentare = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE reprezintă interesele studenților {reprezentare}, asigurându-se că vocea acestora este auzită în toate structurile relevante."

            elif identified_entity == "SUSTINERE_ACTIVITATE_USASE":
                sustinere = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE sprijină activitatea {sustinere}, contribuind la realizarea obiectivelor comune și la îmbunătățirea experienței studențești."

            elif identified_entity == "CONTRACTE_OPERATIUNI_FINANCIARE":
                contracte = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE stabilește contractele pentru operațiuni financiare {contracte}, asigurând transparența și eficiența proceselor financiare."

            elif identified_entity == "COOPERARE_INTERNATIONALA_PROCEDURA":
                cooperare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Procedura de cooperare internațională a ASE se stabilește {cooperare}, facilitând schimbul de cunoștințe și experiențe cu instituții din întreaga lume."

            elif identified_entity == "PARTICIPARE_ASOCIATII_CONSORTII":
                participare_asociatii = results["results"]["bindings"][0]['value']['value']
                results_text = f"ASE participă în asociații sau consorții cu alte instituții {participare_asociatii}, promovând colaborarea și parteneriatul în domeniul educației și cercetării."

            elif identified_entity == "PROMOVARE_VALORI_EDUCATIE_CERCETARE":
                promovare = "activ" if results["results"]["bindings"][0]['value']['value'] == "true" else "pasiv"
                results_text = f"ASE promovează activ valorile spațiului european de învățământ superior și cercetare științifică, contribuind la avansarea standardelor academice și la inovarea în cercetare."

            elif identified_entity == "ALEGERE_REPREZENTANTI_STUDENTI":
                alegeri = results["results"]["bindings"][0]['value']['value']
                results_text = f"Reprezentanții studenților în structurile ASE sunt aleși {alegeri}."

            elif identified_entity == "DESEMNARE_MEMBRI_REPREZENTANTI":
                desemnare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Metodologia pentru desemnarea membrilor reprezentanți ai studenților urmează {desemnare}."

            elif identified_entity == "PARTICIPARE_PROCES_DECIZIONAL":
                participare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Studenții sunt implicați {participare} în procesul decizional din ASE."

            elif identified_entity == "ROL_STUDENTI_DESEMNARE_RECTOR":
                rol = results["results"]["bindings"][0]['value']['value']
                results_text = f"Studenții au un rol important {rol} în procesul de desemnare a Rectorului ASE."

            elif identified_entity == "REPREZENTANT_CONSILIU_ADMINISTRATIE":
                reprezentant = results["results"]["bindings"][0]['value']['value']
                results_text = f"Reprezentantul studenților în Consiliul de Administrație al ASE este {reprezentant}."

            elif identified_entity == "GESTIUNE_PROTEJARE_RESURSE":
                gestiune = results["results"]["bindings"][0]['value']['value']
                results_text = f"Resursele în ASE sunt gestionate și protejate {gestiune}."

            elif identified_entity == "MASURI_ADMINISTRARE_RESURSE":
                masuri = results["results"]["bindings"][0]['value']['value']
                results_text = f"Măsurile de administrare a resurselor materiale și financiare în ASE sunt aplicate {masuri}."

            elif identified_entity == "RECUPERARE_PREJUDICII_PATRIMONIU":
                recuperare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Prejudiciile aduse patrimoniului ASE sunt recuperate {recuperare}."

            elif identified_entity == "APLICABIL_PERSONAL_DIDACTIC":
                aplicabil = results["results"]["bindings"][0]['value']['value']
                results_text = f"Sancțiunile în cadrul personalului didactic din ASE se aplică {aplicabil}."

            elif identified_entity == "TIPURI_SANCTIUNI_PERSONAL_DIDACTIC":
                sancțiuni = [format_property_name(result['property']['value'].split("#")[-1]) for result in
                             results["results"]["bindings"]]
                sancțiuni_text = ', '.join(sancțiuni)
                results_text = f"Tipurile de sancțiuni aplicabile personalului didactic în ASE includ: {sancțiuni_text}."

            elif identified_entity == "APLICABIL_STUDENTI":
                aplicabil = results["results"]["bindings"][0]['value']['value']
                results_text = f"Sancțiunile în rândul studenților ASE se aplică {aplicabil}."

            elif identified_entity == "TIPURI_SANCTIUNI_STUDENTI":
                sancțiuni = [format_property_name(result['property']['value'].split("#")[-1]) for result in
                             results["results"]["bindings"]]
                sancțiuni_text = ', '.join(sancțiuni)
                results_text = f"Tipurile de sancțiuni aplicabile studenților în ASE includ: {sancțiuni_text}."

            elif identified_entity == "DIZOLVARE_SENAT":
                dizolvare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Dizolvarea Senatului în exercițiu din ASE are loc {dizolvare}."

            elif identified_entity == "ORGANIZARE_REFERENDUM":
                organizare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Referendumul pentru desemnarea Rectorului în ASE se organizează {organizare}."

            elif identified_entity == "ELABORARE_METODOLOGIE_ALEGERI":
                termen = results["results"]["bindings"][0]['value']['value']
                results_text = f"Metodologia alegerilor în ASE trebuie elaborată {termen}."

            elif identified_entity == "APLICABIL_PERSONAL_DIDACTIC":
                aplicabil = results["results"]["bindings"][0]['value']['value']
                results_text = f"Sancțiunile în cadrul personalului didactic din ASE se aplică {aplicabil}."

            elif identified_entity == "TIPURI_SANCTIUNI_PERSONAL_DIDACTIC":
                sancțiuni = [format_property_name(result['property']['value'].split("#")[-1]) for result in
                             results["results"]["bindings"]]
                sancțiuni_text = ', '.join(sancțiuni)
                results_text = f"Tipurile de sancțiuni aplicabile personalului didactic în ASE includ: {sancțiuni_text}."

            elif identified_entity == "APLICABIL_STUDENTI":
                aplicabil = results["results"]["bindings"][0]['value']['value']
                results_text = f"Sancțiunile în rândul studenților ASE se aplică {aplicabil}."

            elif identified_entity == "TIPURI_SANCTIUNI_STUDENTI":
                sancțiuni = [format_property_name(result['property']['value'].split("#")[-1]) for result in
                             results["results"]["bindings"]]
                sancțiuni_text = ', '.join(sancțiuni)
                results_text = f"Tipurile de sancțiuni aplicabile studenților în ASE includ: {sancțiuni_text}."

            elif identified_entity == "DIZOLVARE_SENAT":
                dizolvare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Dizolvarea Senatului în exercițiu din ASE are loc {dizolvare}."

            elif identified_entity == "ORGANIZARE_REFERENDUM":
                organizare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Referendumul pentru desemnarea Rectorului în ASE se organizează {organizare}."

            elif identified_entity == "ELABORARE_METODOLOGIE_ALEGERI":
                termen = results["results"]["bindings"][0]['value']['value']
                results_text = f"Metodologia alegerilor în ASE trebuie elaborată {termen}."

            elif identified_entity == "ADOPTARE_REGULAMENT":
                termen = results["results"]["bindings"][0]['value']['value']
                results_text = f"Regulamentul trebuie adoptat de Senatul Universitar ASE {termen} după alegerea Președintelui."

            elif identified_entity == "ATRIBUTII_APROBARE_ACTIVITATI":
                atributii = [format_property_name(result['property']['value'].split("#")[-1]) for result in
                             results["results"]["bindings"]]
                atributii_text = ', '.join(atributii)
                results_text = f"Senatul Universitar are atribuții în aprobarea activităților didactice și de cercetare, inclusiv: {atributii_text}."

            elif identified_entity == "STRUCTURA_SENATULUI":
                structura = results["results"]["bindings"][0]['value']['value']
                results_text = f"Senatul Universitar ASE este structurat {structura}."

            elif identified_entity == "CONDITII_REPREZENTARE_STUDENTI":
                conditii = results["results"]["bindings"][0]['value']['value']
                results_text = f"Condițiile de reprezentare a studenților în Senatul Universitar ASE sunt stabilite prin {conditii}."

            elif identified_entity == "CONDUCERE_SENAT":
                conducere = results["results"]["bindings"][0]['value']['value']
                results_text = f"Senatul Universitar ASE este {conducere}."

            elif identified_entity == "GARANTII_SENAT":
                garanteaza = results["results"]["bindings"][0]['value']['value']
                results_text = f"Senatul Universitar ASE garantează {garanteaza}."

            elif identified_entity == "DURATA_MANDAT_SENAT":
                durata = results["results"]["bindings"][0]['value']['value']
                results_text = f"Durata mandatului membrilor Senatului Universitar ASE este de {durata} ani."

            elif identified_entity == "ORGANIZARE_SEDINTE":
                sedinte = results["results"]["bindings"][0]['value']['value']
                results_text = f"Ședințele Senatului Universitar ASE sunt organizate {sedinte}."

            elif identified_entity == "CALITATEA_DE_STUDENT":
                calitate = results["results"]["bindings"][0]['value']['value']
                results_text = f"Calitatea de student la ASE se obține prin {calitate}."

            elif identified_entity == "CONDITII_FINANTARE":
                finantare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Condițiile de finanțare pentru studenții ASE sunt stabilite {finantare}."

            elif identified_entity == "SUBVENTIE_FINANCIARA":
                subventie = results["results"]["bindings"][0]['value']['value']
                results_text = f"Subvenția financiară pentru studenți se aplică {subventie}."

            elif identified_entity == "COORDONARE_ACTIVITATE":
                coordonare = results["results"]["bindings"][0]['value']['value']
                results_text = f"Activitatea în structurile serviciilor tehnico-administrative ASE este coordonată de {coordonare}."

            elif identified_entity == "STRUCTURI_EDUCATIE_CERCETARE":
                structuri_items = set()

                for result in results["results"]["bindings"]:
                    for prop in entity_mapping["STRUCTURI_EDUCATIE_CERCETARE"]["node_properties"]:
                        if prop in result and result[prop]['value'].lower() == "true":
                            formatted_name = format_property_name(prop)
                            structuri_items.add(formatted_name)

                structuri_list = sorted(list(structuri_items))
                structuri_text = ', '.join(structuri_list)
                results_text = f"Structurile de educație și cercetare existente în ASE includ: {structuri_text}."

            elif identified_entity == "STRUCTURA_SERVICII_TEHNICO_ADMINISTRATIVE":
                structura_items = set()

                for result in results["results"]["bindings"]:
                    for prop in entity_mapping["STRUCTURA_SERVICII_TEHNICO_ADMINISTRATIVE"]["node_properties"]:
                        if prop in result and result[prop]['value'].lower() == "true":
                            formatted_name = format_property_name(prop)
                            structura_items.add(formatted_name)

                structura_list = sorted(list(structura_items))
                structura_text = ', '.join(structura_list)
                results_text = f"Structura serviciilor tehnico-administrative ASE include: {structura_text}."

            elif identified_entity == "STRUCTURI_CONDUCERE":
                structuri = [format_property_name(result['property']['value'].split("#")[-1]) for result in
                             results["results"]["bindings"]]
                structuri_text = ', '.join(structuri)
                results_text = f"Structurile de conducere incluse în ASE sunt: {structuri_text}."

            elif identified_entity == "VALORI_FUNDAMENTALE":
                valori = []

                for result in results["results"]["bindings"]:
                    property_name = format_property_name(result['property']['value'].split("#")[-1])
                    description = result['value']['value']
                    valori.append(f"{description}")

                valori_text = '; '.join(valori)
                results_text = f"Valorile fundamentale promovate de ASE includ: {valori_text}."

            elif identified_entity == "DEFINITIE_INTEGRITATE":
                definitie = results["results"]["bindings"][0]['value']['value']
                results_text = f"Integritatea în cadrul valorilor ASE este definită ca {definitie}."

            elif identified_entity == "PROFESIONALISM":
                profesionalism = results["results"]["bindings"][0]['value']['value']
                results_text = f"Profesionalismul pentru ASE înseamnă {profesionalism}."


            elif identified_entity == "ASIGURAREA_CALITATII":
                asigurare_calitate = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if asigurare_calitate == "true":
                    results_text = "Calitatea în cadrul ASE este asigurată prin standarde înalte de educație și cercetare."
                else:
                    results_text = "Nu există informații disponibile despre asigurarea calității în cadrul ASE."


            elif identified_entity == "AUTONOMIA_UNIVERSITARA":
                autonomia_universitara = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if autonomia_universitara == "true":
                    results_text = "Autonomia universitară pentru ASE înseamnă independența în gestionarea resurselor și deciziilor academice."
                else:
                    results_text = "Nu există informații disponibile despre autonomia universitară în cadrul ASE."


            elif identified_entity == "CENTRAREA_EDUCATIEI_PE_STUDENT":
                centrarea_pe_student = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if centrarea_pe_student == "true":
                    results_text = "Centrarea educației pe student în ASE este realizată prin adaptarea continuă a programelor de studiu la nevoile acestora."
                else:
                    results_text = "Nu există informații disponibile despre centrarea educației pe student în cadrul ASE."

            elif identified_entity == "EFICACITATEA_MANAGERIALA_SI_EFICIENTA_FINANCIARA":

                eficacitate_eficienta = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if eficacitate_eficienta == "true":
                    results_text = "Eficacitatea managerială și eficiența financiară în ASE sunt guvernate de principii de transparență și responsabilitate."
                else:
                    results_text = "Nu există informații disponibile despre eficacitatea managerială și eficiența financiară în cadrul ASE."


            elif identified_entity == "INDEPENDENTA_FATA_DE_IDEOLOGII":

                independenta_ideologii = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if independenta_ideologii == "true":
                    results_text = "Independența față de ideologii în ASE este promovată prin susținerea libertății de exprimare și gândire critică."
                else:
                    results_text = "Nu există informații disponibile despre independența față de ideologii în cadrul ASE."

            elif identified_entity == "LIBERTATEA_ACADEMICA":

                libertatea_academica = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if libertatea_academica == "true":
                    results_text = "Libertatea academică în ASE este susținută prin promovarea cercetării libere și a exprimării fără constrângeri."
                else:
                    results_text = "Nu există informații disponibile despre libertatea academică în cadrul ASE."


            elif identified_entity == "LIBERTATEA_DE_MOBILITATE":

                libertatea_mobilitate = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if libertatea_mobilitate == "true":
                    results_text = "Libertatea de mobilitate pentru comunitatea ASE înseamnă facilitarea schimburilor academice și accesul la programe internaționale."
                else:
                    results_text = "Nu există informații disponibile despre libertatea de mobilitate în cadrul ASE."


            elif identified_entity == "PARTENERIATUL_CU_ENTITATI":

                parteneriat_entitati = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if parteneriat_entitati == "true":
                    results_text = "Parteneriatul cu entități externe în ASE este valorizat prin colaborări care extind impactul educației și cercetării."
                else:
                    results_text = "Nu există informații disponibile despre parteneriatul cu entități externe în cadrul ASE."

            elif identified_entity == "TRANSPARENTA_DECIZIONALA":

                transparenta_decizionala = "true" if results["results"]["bindings"][0]['value']['value'] == "true" else "false"

                if transparenta_decizionala == "true":
                    results_text = "Transparența decizională în ASE este asigurată prin implicarea comunității academice în procesele de luare a deciziilor."
                else:
                    results_text = "Nu există informații disponibile despre transparența decizională în cadrul ASE."


    user_question = request.form.get('question')
    user_id = get_current_user()
    is_logged_in = bool(user_id)
    if is_logged_in:
        if 'chat_history' not in session:
            session['chat_history'] = []
        session['chat_history'].append({'type': 'user', 'text': user_question})
        session['chat_history'].append({'type': 'response', 'text': results_text})
        session.modified = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return results_text
    else:
        return render_template('chat.html', chat_history=session.get('chat_history', []))
