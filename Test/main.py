import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

chromedriver_path = "C:\\Users\\alexm\\Desktop\\chromedriver.exe"

try:
    service = Service(executable_path=chromedriver_path)
    driver = webdriver.Chrome(service=service, options=options)
except Exception as e:
    print(f"Failed to initialize WebDriver: {e}")
    sys.exit(1)

url = 'http://127.0.0.1:5000/chat'
driver.get(url)

questions = [
    #  NIVEL_ACREDITARE
    "Care este nivelul de acreditare al ASE?",
    "Ce grad de acreditare are ASE?",
    "Nivel acreditare ASE",

    #  CARACTER_UNIVERSITATE
    "Ce caracter distinctiv are ASE?",
    "Cum se distinge ASE?",
    "Caracter ASE",

    #  DENUMIRE_OFICIALA
    "Cum se numeste oficial ASE?",
    "Care este denumirea completa a ASE?",
    "Nume oficial ASE"

    #  LOCATIE_SEDIU
    "Unde se afla sediul ASE?",
    "Locatia sediului ASE",
    "Adresa ASE",

    #  SITE_WEB
    "Care este site-ul ASE?",
    "Pagina web ASE",
    "ASE online",

    #  DENUMIRE_ENGLEZA
    "Cum se numeste ASE in engleza?",
    "ASE English",
    "Nume englez ASE"  
    
    #  LEGE_INFIINTARE
    "Care este legea de infiintare a ASE?",
    "Actul de constituire ASE?",
    "Legea ASE",

    #  INFIINTARE_ASE
    "Cum a fost infiintata ASE?",
    "Infiintarea ASE",
    "Istoria inceputurilor ASE",

    #  DECRET_REGAL
    "Care este decretul regal al ASE?",
    "Decret regal ASE",
    "Act regal ASE"

    #  PROMULGATOR
    "Cine a ratificat infiintarea ASE?",
    "Promulgator ASE",
    "Cine a semnat actul de fondare ASE?",

    #  DATA_SARBATOARE
    "Care este data comemorativa pentru ASE?",
    "Ziua ASE",
    "Cand sarbatoreste ASE fondarea?",

    #  TIP_DISCRIMINARE
    "Ce forme de discriminare sunt recunoscute in ASE?",
    "Discriminare ASE",
    "Tipuri de discriminare in ASE"  
    
    #  ABATERE_ETICA
    "Care sunt abaterile etice recunoscute la ASE?",
    "Abateri etice ASE",
    "Cum sunt gestionate abaterile etice in ASE?",

    #  ACTIVITATE_NENUMARATA
    "Care sunt efectele activitatii neremunerate la ASE?",
    "Activitate neremunerata ASE",
    "Impactul activitatii neremunerate asupra cadrelor didactice",

    #  ABATERE_GRAVA
    "Ce abateri grave au fost sanctionate la ASE?",
    "Abateri grave ASE",
    "Cum sunt gestionate abaterile grave in ASE?",

    #  APROBATOR_SPATII
    "Cine aproba utilizarea spatiilor pentru evenimente ASE?",
    "Aprobare spatii evenimente ASE",
    "Responsabil spatii conferinte",

    #  INCURAJARE_ACTIVITATI
    "Ce activitati studentesti sunt incurajate de ASE?",
    "Activitati studentesti ASE",
    "Proiecte studentesti incurajate",

    #  PLANIFICARE_EVENIMENTE
    "Cum organizeaza ASE evenimentele sportive anuale?",
    "Planificare evenimente ASE",
    "Organizare activitati ASE",

    #  TIP_EVENIMENTE
    "Ce evenimente culturale organizeaza ASE pentru studenti?",
    "Evenimente studentesti ASE",
    "Tipuri evenimente ASE",

    #  PARTENERI_ORGANIZATII
    "Ce tip de parteneri are ASE pentru proiectele sale?",
    "Parteneri ASE evenimente",
    "Organizatii colaboratoare ASE",

    #  RESPONSABIL_ORGANIZARE
    "Cine este responsabil pentru organizarea evenimentelor in ASE?",
    "Responsabil organizare evenimente ASE",
    "Organizator evenimente ASE",

    #  SUSTINERE_ACTIVITATI
    "Cum ofera ASE suport pentru activitatile studentesti?",
    "Suport activitati ASE",
    "ASE suport extracurricular",

    #  RATIFICATOR_CARTE
    "Cine ratifica modificarile Cartei ASE?",
    "Ratificare modificari Carta",
    "Semnare actualizari Carta",

    #  INITIATOR_AMENDA
    "Cine poate initia amendamente pentru Carta ASE?",
    "Initiator amendamente Carta",
    "Propunere amendamente Carta",

    #  EXECUTOR_SANCTIUNI
    "Cine este executorul sanctiunilor in ASE?",
    "Executor sanctiuni ASE",
    "Gestiune sanctiuni ASE",

    #  TERMEN_SANCTIUNI
    "Ce termen are Rectorul ASE pentru sanctiunile aplicate?",
    "Termen sanctiuni ASE",
    "Deadline sanctiuni ASE",

    #  AUTONOMIE_DIDACTICA
    "Ce reprezinta autonomia didactica in ASE?",
    "Principii autonomie didactica",
    "Definire autonomie didactica",

    #  AUTONOMIE_FINANCIARA
    "Cum este definita autonomia financiara la ASE?",
    "Elemente autonomie financiara",
    "Structura autonomie financiara",

    #  AUTONOMIE_FUNCTIONALA
    "Ce inseamna autonomia functionala pentru ASE?",
    "Caracteristici autonomie functionala",
    "Aplicare autonomie functionala",

    #  CHELTUIELI_LEGE
    "Ce norme trebuie urmate la ASE pentru cheltuieli conforme cu legea?",
    "Reguli legale cheltuieli ASE",
    "Gestionare cheltuieli legale",

    #  DEZVOLTARE_BAZA_MATERIALA
    "Cum se initiaza si se valideaza extinderea bazei materiale la ASE?",
    "Dezvoltare baza materiala ASE",
    "Extindere baza materiala ASE",

    #  PRINCIPII_GESTIONARE
    "Care sunt principiile de gestionare a resurselor la ASE?",
    "Principii gestionare ASE",
    "Norme gestionare resurse ASE",

    #  UTILIZARE_SPONSORIZARI
    "Cum sunt folosite resursele din sponsorizari la ASE?",
    "Utilizare resurse sponsorizate ASE",
    "Gestionare fonduri sponsorizari",

    #  MINIMIZARE_HARTUIRE
    "Cum sunt gestionate temerile de hartuire sexuala la ASE?",
    "Strategii reducere hartuire sexuala ASE",
    "Prevenire hartuire sexuala ASE",

    #  MOD_SOLUTIE
    "Cum sunt gestionate disputele la ASE?",
    "Metode rezolvare dispute ASE",
    "Strategii solutii ASE",

    #  PROTEJARE_IDENTITATE
    "Cum asigura ASE anonimatul celor afectati in incidente?",
    "Protejare identitate victime",
    "Confidentialitate victime",

    #  PROTEJARE_IDENTITATE
    "Cum protejeaza ASE identitatea victimelor?",
    "Mecanisme ASE pentru confidentialitate",
    "Confidentialitate ASE",

    #  ATRIBUTII_COMISIA_ETICA
    "Ce responsabilitati are Comisia de Etica la ASE?",
    "Functii Comisia de Etica ASE",
    "Atributii Comisia de Etica",

    #  COMPOZITIE_COMISIA_ETICA
    "Cine sunt membrii Comisiei de Etica la ASE?",
    "Componența Comisiei de Etica ASE",
    "Membri Comisia de Etica",

    #  CONSTITUIRE_COMISIA_ETICA
    "Cum se constituie Comisia de Etica si Deontologie la ASE?",
    "Proces de formare Comisia de Etica ASE",
    "Formare Comisia Etica",

    #  EXCLUDERE_COMISIA_ETICA
    "Ce restrictii exista pentru membrii Comisiei de Etica ASE?",
    "Criterii de excludere din Comisia de Etica ASE",
    "Excludere Comisia Etica",

    #  HOTARARI_COMISIA_ETICA
    "Cum se valideaza deciziile Comisiei de Etica ASE?",
    "Proces de avizare hotarari Comisia de Etica ASE",
    "Validare hotarari Comisia Etica",

    #  CALITATE_CERCETATOR_POSTDOCTORAT
    "Ce criterii trebuie sa indeplineasca un cercetator postdoctorat la ASE?",
    "Calificari necesare pentru cercetator postdoctorat ASE",
    "Cercetator postdoctorat ASE",

    #  CALITATE_CURSANT
    "Cine poate fi cursant la ASE?",
    "Definitie cursant ASE",
    "Cursant ASE",

    #  CALITATE_PERSONAL_DIDACTIC
    "Ce standarde trebuie sa indeplineasca personalul didactic ASE?",
    "Calitatea personalului didactic ASE",
    "Personal didactic ASE",

    #  CALITATE_STUDENTI
    "Ce defineste statutul studentilor la ASE?",
    "Criterii pentru statutul studentilor ASE",
    "Statut studenti ASE",

    #  ATRIBUTII_PERSONAL
    "Ce responsabilitati are personalul universitar ASE?",
    "Atributii personal universitar ASE",
    "Personal universitar ASE",

    #  COLABORARE_VIZIUNE_MISIUNE
    "Cum se manifesta colaborarea pentru viziune si misiune la ASE?",
    "Principii colaborare viziune si misiune ASE",
    "Colaborare viziune ASE",

    #  DIALOG_SOCIAL
    "Ce rol are ASE in dialogul social?",
    "Mecanisme de dialog social la ASE",
    "Dialog social ASE",

    #  EQUIVALARE_FUNCTII
    "Ce reguli guverneaza echivalarea functiilor la ASE?",
    "Proces de echivalare a functiilor didactice si de cercetare ASE",
    "Echivalare functii ASE",

    #  STRUCTURARE_COMUNITATE
    "Cum este structurata comunitatea ASE?",
    "Principii structurare comunitate ASE",
    "Structura comunitate ASE",

    #  STRUCTURA_CERCETATORI_POSTDOCTORAT
    "Cum sunt organizati cercetatorii postdoctorat la ASE?",
    "Structura cercetatori postdoctorat ASE",
    "Organizare cercetatori postdoctorat",

    #  STRUCTURA_CURSANTI
    "Cum sunt inclusi cursantii in comunitatea ASE?",
    "Structura cursanti ASE",
    "Organizare cursanti ASE",

    #  STRUCTURA_PERSONAL_DIDACTIC
    "Cum este organizat personalul didactic la ASE?",
    "Structura personal didactic ASE",
    "Organizare personal didactic",

    #  STRUCTURA_PERSONAL_DIDACTIC_AUXILIAR
    "Cum sunt organizati asistentii de laborator la ASE?",
    "Structura personal didactic auxiliar ASE",
    "Organizare cadre didactice auxiliare",

    #  STRUCTURA_STUDENTI
    "Cum sunt organizati studentii in programele ASE?",
    "Structura studenti ASE",
    "Organizare studenti",

    #  CONFLICT_INTERESE_DECIZII_ACTE
    "Cum sunt gestionate conflictele de interese la ASE?",
    "Conflict de interese in acte decizionale",
    "Gestionare conflict interese",

    #  INCOMPATIBILITATI_CONFLICT_INTERESE
    "Cum sunt gestionate incompatibilitatile si conflictele de interese?",
    "Incompatibilitati si conflicte de interese ASE",
    "Gestionare incompatibilitati",

    #  INFLUENTA_INDEPLINIRE_ATRIBUTII
    "Cum influenteaza regulile indeplinirea atributiilor?",
    "Influenta indeplinire atributii ASE",
    "Regulament influenta atributii",

    #  INTERES_PERSONAL
    "Cum afecteaza interesul personal deciziile ASE?",
    "Impactul interesului personal la ASE",
    "Gestionare interes personal",

    #  OBLIGATIE_INFORMARE
    "Ce obligatii de informare exista la ASE?",
    "Obligatie informare conflict interese",
    "Reguli informare ASE",

    #  SITUATIE_CONFLICT
    "Cum este definit un conflict de interese la ASE?",
    "Situatie conflict interese ASE",
    "Definire conflict interese",

    #  VERIFICARE_CONFLICT
    "Cum se verifica conflictele de interese la ASE?",
    "Verificare conflict interese ASE",
    "Procedura verificare conflict",

    #  ANALIZA_PLANURI_INVATAMANT
    "Cum se analizeaza planurile de invatamant in ASE?",
    "Proceduri analiza planuri invatamant",
    "Analiza planuri ASE",

    #  APROBARE_CERERI_CONCEDII
    "Cum se aproba cererile de concedii in ASE?",
    "Proces aprobare concedii",
    "Aprobare concedii",

    #  APROBARE_CONCURS_POSTURI
    "Cum se aproba concursurile de posturi in ASE?",
    "Proceduri aprobare concurs posturi",
    "Aprobare concurs posturi",

    #  APROBARE_OPERATIUNI_FINANCIARE
    "Cum se aproba operatiunile financiare in ASE?",
    "Proceduri aprobare operatiuni financiare",
    "Operatiuni financiare",

    #  AVIZARE_EXAMEN_MEDICAL
    "Cum se avizeaza examenele medicale in ASE?",
    "Proceduri avizare examen medical",
    "Avizare examene medicale",

    #  AVIZARE_RAPORT_REGIE
    "Cum se avizeaza rapoartele in ASE?",
    "Proceduri avizare raport financiar",
    "Avizare raport",

    #  ELABORARE_BUGET_BILANT
    "Cum se elaboreaza bugetul si bilantul in ASE?",
    "Proces elaborare buget",
    "Elaborare buget",

    #  ELABORARE_REGULAMENTE_METODOLOGII
    "Cum se elaboreaza regulamentele si metodologiile in ASE?",
    "Proceduri elaborare regulamente",
    "Elaborare regulamente",

    #  INDEPLINIRE_ALTE_ATRIBUTII
    "Ce alte atributii indeplineste Consiliul in ASE?",
    "Responsabilitati suplimentare Consiliu",
    "Atributii Consiliu",

    #  ORGANIZARE_CONCURS_DIRECTOR
    "Cum se organizeaza concursul pentru director in ASE?",
    "Proceduri organizare concurs director",
    "Organizare concurs",

    #  PROPUNERE_AN_SABATIC
    "Cum se propune anul sabatic in ASE?",
    "Proceduri propunere an sabatic",
    "Propunere an sabatic",

    #  PROPUNERE_COMISIE_ETICA
    "Cum se propune comisia de etica in ASE?",
    "Criterii propunere comisie etica",
    "Propunere comisie etica",

    #  STABILIRE_PARTENERIATE
    "Cum se stabilesc parteneriatele in ASE?",
    "Proceduri stabilire parteneriate",
    "Parteneriate ASE",

    #  VALIDARE_COMISIE_CONCURS
    "Cum se valideaza comisiile de concurs in ASE?",
    "Procedura validare comisie concurs",
    "Validare comisii",

    #  ALEGERI_CONSILIUL_DEPARTAMENTULUI
    "Cum se aleg membrii Consiliului Departamentului in ASE?",
    "Procedura alegeri Consiliul Departamentului",
    "Alegeri Consiliul",

    #  REGULAMENT_CONSILIUL_DEPARTAMENTULUI
    "Există un regulament pentru Consiliul Departamentului in ASE?",
    "Norme functionare Consiliul Departamentului",
    "Regulament Consiliul",

    #  ALEGERI_CONSILIUL_FACULTATII
    "Cum se aleg membrii Consiliului Facultatii in ASE?",
    "Procedura alegeri Consiliul Facultatii",
    "Alegeri Consiliul Facultatii",

    #  ATRIBUTII_CONSILIUL_FACULTATII
    "Ce atributii are Consiliul Facultatii in ASE?",
    "Responsabilitati Consiliul Facultatii",
    "Atributii Consiliul",

    #  COMPOZITIE_CONSILIUL_FACULTATII
    "Cum este compus Consiliul Facultatii in ASE?",
    "Structura Consiliul Facultatii",
    "Compozitie Consiliul",

    #  CONDITII_MEMBRI_STUDENTI
    "Ce conditii trebuie sa indeplineasca studentii in Consiliul Facultatii?",
    "Criterii pentru studenti in Consiliul Facultatii",
    "Studenti Consiliul",

    #  QUORUM_CONSILIUL_FACULTATII
    "Ce quorum este necesar pentru Consiliul Facultatii?",
    "Reguli de quorum pentru Consiliul Facultatii",
    "Quorum Consiliul",

    #  SEDINTE_CONDUCERE_CONSILIUL_FACULTATII
    "Cine conduce sedintele Consiliului Facultatii?",
    "Liderul sedintelor Consiliul Facultatii",
    "Conducere sedinte",

    #  SEDINTE_FRECVENTA_CONSILIUL_FACULTATII
    "Cat de des are loc Consiliul Facultatii?",
    "Frecventa sedintelor Consiliul Facultatii",
    "Sedinte Consiliul",

    #  VOT_CONSILIUL_FACULTATII
    "Cum se realizeaza votul in Consiliul Facultatii?",
    "Procedura de vot in Consiliul Facultatii",
    "Vot Consiliul",

    #  ALEGERI_CONSILIUL_SCOLII_DOCTORALE
    "Cum se aleg membrii Consiliului Scolii Doctorale?",
    "Procesul de alegeri in Consiliul Scolii Doctorale",
    "Alegeri Consiliul Doctoral",

    #  REGULAMENT_CONSILIUL_SCOLII_DOCTORALE
    "Există un regulament pentru functionarea Consiliului Scolii Doctorale?",
    "Normele de functionare ale Consiliului Scolii Doctorale",
    "Regulament Consiliul Doctoral",

    #  ATRIBUTII_C_S_U_DOCTORAT
    "Ce atributii are Consiliul Studiilor Universitare de Doctorat?",
    "Responsabilitati ale Consiliului Studiilor Universitare de Doctorat",
    "Atributii CSU Doctorat",

    #  COORDONARE_PARTENERIATE
    "Cum se coordoneaza parteneriatele pentru scolile doctorale?",
    "Metode de coordonare a parteneriatelor la scolile doctorale",
    "Coordonare parteneriate"

#  CONDITII_MEMBRI_CADRE_DIDACTICE
    "Cine poate face parte din cadrele didactice ale Consiliului Studiilor Universitare de Doctorat?",
    "Eligibilitate cadre didactice Consiliul Doctorat",
    "Cadre Consiliul Doctoratului",

    #  DESEMNARE_DIRECTOR
    "Cum se desemnează directorul Consiliului Studiilor Universitare de Doctorat în ASE?",
    "Procedura alegere director Doctorat",
    "Director Consiliul Doctoratului",

    #  MANDAT_CADRE_DIDACTICE
    "Care este mandatul cadrelor didactice în cadrul Consiliului Studiilor Universitare de Doctorat?",
    "Durata mandatului cadrelor didactice",
    "Mandat cadre",

    #  NUMAR_MEMBRI
    "Câte persoane fac parte din Consiliul Studiilor Universitare de Doctorat în ASE?",
    "Numar membri Consiliul Doctoratului",
    "Membri Consiliul Doctorat",

    #  DATA_APROBARE
    "Când a fost aprobată ultima modificare în ASE?",
    "Data ultimei aprobări ASE",
    "Ultima aprobare",

    #  DATA_MODIFICARE
    "Când a avut loc ultima modificare a regulamentelor ASE?",
    "Ultima revizie a regulamentului ASE a fost când?",
    "Ultima modificare",

    #  VIGOARE
    "Ce condiție trebuie îndeplinită pentru intrarea în vigoare a modificărilor ASE?",
    "Cand intra in vigoare modificari",
    "intrare vigoare",

    #  MEMBRU_DREPT_CONSILIU_ADMINISTRATIE
    "Este Decanul membru de drept în Consiliul de Administrație al ASE?",
    "Decanul in Consiliul de Administratie",
    "Decan Consiliu",

    #  SITUATII_DEMISIE_DECAN
    "În ce situații poate fi demis Decanul în ASE?",
    "Cazuri de demitere a Decanului",
    "Demitere Decan",

    #  RESPONSABILITATI_MANAGEMENT_FACULTATE
    "Ce responsabilități are Decanul în gestionarea facultății în ASE?",
    "Rolul Decanului in gestionarea facultatii",
    "Decan responsabilitati",

    #  SARCINI_DECAN
    "Ce sarcini are Decanul în cadrul facultății din ASE?",
    "Rolurile Decanului în facultate",
    "Decan sarcini",

    #  SELECTIE_DECAN
    "Cum este selectat Decanul facultății în ASE?",
    "Procesul de selectie a Decanului",
    "Selectie Decan",

    #  DEMNITATE_CONDUITA_DEONTOLOGIA
    "Ce caracterizează demnitatea și conduita în deontologia universitară ASE?",
    "Principii de demnitate in deontologie",
    "Demnitate ASE"  
    
    #  PRODUCEREA_CUNOASTERII
    "Cum se asigură producerea cunoașterii în departamentele ASE?",
    "Procese de cunoastere la ASE",
    "Cunoastere ASE",

    #  CONDUCERE_DEPARTAMENT
    "Cum este condus un departament în ASE?",
    "Conducerea departamentelor ASE",
    "Conducere departament",

    #  INFIINTARE_DEPARTAMENT
    "Cum se înființează departamentele în ASE?",
    "Infiintare departament ASE",
    "Infiintare departament",

    #  STRUCTURA_DEPARTAMENT
    "Care sunt structurile incluse în cadrul unui departament ASE?",
    "Structura departament ASE",
    "Structura departament",

    #  FUNCTIE_DIRECTOR_CSUD
    "Ce funcție de conducere ocupă Directorul CSUD în ASE?",
    "Functia Directorului CSUD ASE",
    "Functie CSUD",

    #  SUBORDONAT_DIRECTOR_GENERAL
    "Cui este subordonat Directorul General Adjunct Administrativ în ASE?",
    "Subordonatii Directorului Adjunct ASE",
    "Subordonatii Adjunct",

    #  CONDUCE_STRUCTURA_ADMINISTRATIVA
    "Cum este condusă structura administrativă ASE de către Directorul General Administrativ?",
    "Conducerea administrativa ASE",
    "Conducere ASE",

    #  OCUPARE_POST_DIRECTOR_GENERAL
    "Cum se ocupă postul de Director General Administrativ în ASE?",
    "Ocuparea postului de DGA in ASE",
    "DGA post",

    #  SITUATII_DEMISIE_DIRECTOR_GENERAL
    "În ce situații poate fi demis Directorul General Administrativ în ASE?",
    "Demiterea DGA ASE",
    "Demitere DGA",

    #  RESPONSABILITATI_GESTIONARE_ECONOMICO_FINANCIARA
    "Ce responsabilități are Directorul General Administrativ în gestionarea economico-financiară în ASE?",
    "DGA responsabilitati economice",
    "DGA finante",

    #  CONDUCERE_OPERATIVA_DEPARTAMENT
    "Cum este condusă activitatea operativă în Departamentul ASE de către Director?",
    "Conducerea operativa de catre Director",
    "Conducere operativa",

#  REVOCARE_DIRECTOR_DEPARTAMENT
    "În ce condiții poate fi revocat Directorul de Departament în ASE?",
    "Revocare Director Departament ASE",
    "Revocare Director",

    #  SARCINI_DIRECTOR_DEPARTAMENT
    "Ce sarcini are Directorul de Departament în ASE?",
    "Sarcini zilnice Director Departament",
    "Sarcini director",

    #  SELECTIE_DIRECTOR_DEPARTAMENT
    "Cum este selectat Directorul de Departament în ASE?",
    "Selectie Director Departament ASE",
    "Selectie Director",

    #  CONDUCERE_OPERATIVA_SCOLI_DOCTORALE
    "Cum asigură Directorul Școlii Doctorale conducerea operativă în ASE?",
    "Conducerea operativa de catre Directorul Scolii Doctorale",
    "Conducere operativa",

    #  REVOCARE_DIRECTOR_SCOLI_DOCTORALE
    "În ce condiții poate fi revocat Directorul Școlii Doctorale în ASE?",
    "Revocare Director Scoli Doctorale",
    "Revocare Director",

    #  SARCINI_DIRECTOR_SCOLI_DOCTORALE
    "Ce sarcini are Directorul Școlii Doctorale în ASE?",
    "Sarcini Director Scoli Doctorale",
    "Sarcini Director",

    #  SELECTIE_DIRECTOR_SCOLI_DOCTORALE
    "Cum este selectat Directorul Școlii Doctorale în ASE?",
    "Selectia Directorului Scoli Doctorale",
    "Selectie Director",

    #  DREPTURI_PERSONAL_DIDACTIC_CERCETARE
    "Ce drepturi are personalul didactic și de cercetare în ASE?",
    "Drepturi cadru didactic si cercetare",
    "Drepturi didactice",

    #  OBLIGATII_PERSONAL_DIDACTIC_CERCETARE
    "Ce obligații are personalul didactic și de cercetare în ASE?",
    "Obligatii cadru didactic si cercetare",
    "Obligatii profesori",

    #  EXPRIMARE_LIBERA_OPINII
    "Este permisă exprimarea liberă a opiniilor pentru personalul didactic și de cercetare în ASE?",
    "Libertatea de exprimare in ASE",
    "Exprimare libera",

    #  MOBILITATE_INTERNATIONALA
    "Cum este reglementată mobilitatea internațională pentru personalul didactic și de cercetare în ASE?",
    "Mobilitate internationala cadru didactic",
    "Mobilitate internationala ASE",

    #  CONCEDIILE_CU_FARA_PLATA
    "Ce condiții sunt pentru concediile cu plată și fără plată pentru personalul didactic și de cercetare în ASE?",
    "Concedii platite si neplatite ASE",
    "Concedii ASE",

    #  PROTECTIE_SPATIU_UNIVERSITAR
    "Cum este protejat spațiul universitar pentru personalul didactic și de cercetare în ASE?",
    "Protectia spatiilor de predare ASE",
    "Protectie spatii ASE",

    #  EVALUARE_PERIODICA
    "Ce presupune evaluarea periodică a personalului didactic și de cercetare în ASE?",
    "Evaluarea performantei academice",
    "Evaluare performanta ASE",

    #  CONTRIBUIRE_MISIUNE_ASE
    "Cum contribuie personalul didactic și de cercetare la misiunea ASE?",
    "Contributia la valorile ASE",
    "Contributie valori ASE",

    # ACCES_HOTARARI
    "Ce drepturi au studenții la accesul informațiilor și la hotărârile structurilor de conducere în ASE?",
    "Acces studenti la hotarari ASE",
    "Acces la informatii ASE",

    # BENEFICIERE_ASISTENTA_MEDICALA
    "Cum pot studenții ASE să beneficieze de asistență medicală și psihologică gratuită?",
    "Asistenta medicala gratuita ASE",
    "Acces asistenta psihologica",

    # BENEFICIERE_CAZARE
    "Ce prevederi legale asigură dreptul la cazare pentru studenții ASE?",
    "Cazare studenti ASE",
    "Cazare subventionata ASE",

    # BENEFICIERE_PROTECTIE_UNIVERSITAR
    "Cum este protejat spațiul universitar pentru studenții ASE?",
    "Protecție campus ASE",
    "Securitate campus ASE",

    # BENEFICIERE_SERVICII
    "Ce facilități și servicii sunt disponibile pentru studenții ASE?",
    "Servicii studentesti ASE",
    "Facilitati studenti ASE",

    # CONTESTARE_NOTE
    "Cum pot studenții ASE să conteste notele obținute?",
    "Contestatii note ASE",
    "Procedura contestare note ASE",

    # PROPRIETATE_INTELECTUALA
    "Ce drepturi au studenții ASE legate de proprietatea intelectuală?",
    "Drepturi proprietate intelectuala",
    "Protejarea creatiilor studentesti",

    # DESFASURARE_ACTIUNI
    "Cum este reglementată participarea studenților ASE la activitățile extracurriculare?",
    "Activitati extracurriculare ASE",
    "Reguli activitati extracurriculare ASE",

    # LIMITARE_ORAR
    "Cum este reglementată limitarea orarului zilnic pentru studenții ASE?",
    "Limitare program zilnic",
    "Reguli orar zilnic studenti ASE",

    # PARTICIPARE_PROCES_ELABORARE_REGULAMENTE
    "Cum pot studenții ASE să participe la procesul de elaborare a regulamentelor universitare?",
    "Participare la regulamente ASE",
    "Contributia studentilor la regulamente",

    # RECUNOASTERE_PRACTICA_INDIVIDUALA
    "Cum este recunoscută practica individuală a studenților ASE?",
    "Recunoasterea practicii ASE",
    "Validare practica studenti ASE",

    # PROTECTIE_DATE_PERSONALE
    "Cum este asigurată protecția datelor personale ale studenților ASE?",
    "Protejarea datelor studenti ASE",
    "Securitatea informatiilor personale studenti",

    # STUDIU_LIMBA_INTERNATIONALA
    "Ce studii gratuite sunt oferite absolvenților din centrele de plasament de către ASE?",
    "Studiu in limba straina ASE",
    "Program limba internationala ASE",

    # SESIZARE_ABUZURI
    "Cum pot studenții ASE să sesizeze abuzurile și neregulile?",
    "Raportare probleme ASE",
    "Sesizare abuzuri ASE",

    # TERMENE_INSCRIERE
    "Ce termene sunt stabilite pentru înscrierea la activitățile universitare în ASE?",
    "Termene inscrieri ASE",
    "Date limita inscriere ASE",

    # UTILIZARE_FACILITATI
    "Cum pot studenții ASE să utilizeze facilitățile universității?",
    "Utilizare spatii ASE",
    "Acces facilitati ASE",

    # STUDII_GRATUITE_CENTRE_PLASAMENT
    "Ce gratuități sunt oferite studenților etnici români în ASE?",
    "Studii gratuite centre plasament ASE",
    "Gratuitati studenti romani ASE",

    # ACCES_ADAPTAT_DIZABILITATI
    "Cum este asigurat accesul adaptat pentru studenții cu dizabilități în ASE?",
    "Acces adaptat studenti cu dizabilitati ASE",
    "Facilitati accesibile ASE",

    # CONDITII_NORMALE_DIZABILITATI
    "Ce condiții sunt create pentru studenții cu dizabilități în ASE?",
    "Conditii pentru studenti cu dizabilitati ASE",
    "Spatii adaptate studenti ASE",

    # BENEFICIERE_LOGISTICA_DOCTORAT
    "Ce resurse logistice sunt disponibile pentru studenții doctoranzi în ASE?",
    "Resurse pentru doctoranzi ASE",
    "ASE resurse doctoranzi",

    # COLABORARE_ECHIPE_CERCETARE
    "Cum pot studenții doctoranzi ASE să colaboreze cu echipe de cercetare?",
    "Colaborari in cercetare",
    "Colaborare cercetare ASE",

    # MOBILITATI_DOCTORAT
    "Ce mobilități sunt disponibile pentru studenții doctoranzi în ASE?",
    "Mobilitate doctoranzi ASE",
    "Oportunitati mobilitate doctorat",

    # REPREZENTARE_FORURI_DOCTORAT
    "Cum sunt reprezentați studenții doctoranzi în forurile decizionale ASE?",
    "Reprezentare doctoranzi in foruri",
    "Rolul doctoranzilor ASE in consilii",

    # GRATUITATE_MANIFESTARI_ROMANI
    "Ce gratuități sunt oferite studenților etnici români în ASE?",
    "Beneficii pentru studentii romani",
    "Gratuitati studenti romani ASE"

    # LOCURI_FINANTATE_MARGINALIZATI
    "Ce locuri finantate sunt pentru candidatii marginalizati in ASE?",
    "Cum sunt sprijiniti studentii marginalizati in ASE?",
    "Finantare studenti marginalizati ASE",

    # SERVICII_URMARIRE_MARGINALIZATI
    "Ce servicii de urmarire sunt pentru studentii marginalizati in ASE?",
    "Cum ajuta ASE la integrarea studentilor marginalizati?",
    "Servicii urmarire marginalizati ASE",

    # EVIDENTA_STUDENTI
    "Cum se tine evidenta studentilor in ASE?",
    "Ce metode sunt pentru evidenta studentilor in ASE?",
    "Evidenta studenti ASE",

    # DEFINITIE_FACULTATE
    "Cum este definita o facultate in ASE?",
    "Ce reprezinta facultatea in structura ASE?",
    "Definitie facultate ASE",

    # ORGANISM_DECIZIONAL_FACULTATE
    "Cine este organismul decizional al unei facultati in ASE?",
    "Cum este structurat organismul decizional in facultatile ASE?",
    "Organism decizional facultate ASE",

    # STRUCTURA_FACULTATE
    "Cum este structurata o facultate in ASE?",
    "Ce structura organizatorica au facultatile din ASE?",
    "Structura facultate ASE",

    # INFIINTARE_FUNCTIONARE_DESFIINTARE_FACULTATE
    "Cum se infiinteaza si se desfiinteaza facultatile in ASE?",
    "Ce reglementari exista pentru functionarea facultatilor in ASE?",
    "Ciclul de viata facultati ASE",

    # CONTRACTE_MINISTER_RESORT
    "Cum este finantata ASE prin contracte cu Ministerul?",
    "Care sunt modalitatile de finantare a ASE prin acorduri ministeriale?",
    "Contracte finantare ASE",

    # FINANTARE_ALTE_SURSE
    "Ce surse de finantare alternative exista pentru ASE?",
    "Cum poate ASE sa acceseze fonduri alternative de finantare?",
    "Finantare alternativa ASE"  
    
# FINANTARE_CERCETARE_STIINTIFICA
    "Cum este finantata cercetarea stiintifica in ASE?",
    "Ce metode de finantare sunt pentru cercetarea stiintifica la ASE?",
    "Finantare cercetare ASE",

    # FINANTARE_TAXE_SCOLARIZARE
    "Cum influenteaza taxele de scolarizare bugetul ASE?",
    "Ce rol au taxele de scolarizare in ASE?",
    "Taxe scolarizare ASE",

    # VENITURI_PROPRII
    "Cum contribuie veniturile proprii la bugetul ASE?",
    "Care este impactul veniturilor proprii asupra ASE?",
    "Venituri ASE",

    # CONFLICT_INTERESE_SITUATII
    "Ce situatii pot genera conflicte de interese in ASE?",
    "Cum sunt gestionate conflictele de interese in ASE?",
    "Conflict interese ASE",

    # INFORMARE_CONFLICT
    "Cum se informeaza despre conflicte de interese in ASE?",
    "Ce metode de notificare a conflictelor exista la ASE?",
    "Informare conflict ASE",

    # REZOLVARE_INCOMPATIBILITATE
    "Ce proceduri sunt pentru rezolvarea incompatibilitatilor in ASE?",
    "Cum se gestioneaza cazurile de incompatibilitate in ASE?",
    "Incompatibilitate ASE",

    # MANIFESTARE_LIBERTATE_ACADEMICA
    "Cum se manifesta libertatea academica in ASE?",
    "Ce forme ia libertatea academica in ASE?",
    "Libertate academica ASE",

    # PERMISE_ACTIVITATI
    "Ce activitati sunt permise in ASE?",
    "Cum sunt reglementate activitatile academice in ASE?",
    "Activitati permise ASE",

    # STUDENTI_IMPLICARE_MANAGEMENT
    "Cum sunt implicati studentii in managementul ASE?",
    "Ce rol au studentii in comitetele de conducere din ASE?",
    "Studenti management ASE",

    # MISIUNE_CERCETARE
    "Care este misiunea de cercetare a ASE?",
    "Cum este definit scopul cercetarii stiintifice in ASE?",
    "Misiune cercetare ASE",

    # MISIUNE_EDUCATIONALA
    "Care este misiunea educationala a ASE?",
    "Ce obiective are misiunea educationala la ASE?",
    "Misiune educationala ASE",

    # MISIUNE_COMUNITATE
    "Cum colaboreaza ASE cu comunitatea locala?",
    "Care sunt parteneriatele ASE cu comunitatea?",
    "ASE comunitate",

    # OBLIGATII_FINANCIARE_STUDENTI
    "Ce obligatii financiare au studentii fata de ASE?",
    "Cum sunt stabilite contributiile financiare ale studentilor?",
    "Obligatii financiare studenti ASE",

    # COMPORTAMENT_CIVIC
    "Cum trebuie sa se comporte studentii in spatiile ASE?",
    "Ce reguli de comportament trebuie respectate de studenti in ASE?",
    "Comportament civic ASE",

    # RESPECTARE_CURATENIE_ORDINE
    "Care sunt normele de curatenie si ordine in caminele ASE?",
    "Cum trebuie sa fie mentinuta curatenia in ASE?",
    "Curatenie si ordine ASE"

    # RESPECTARE_STANDARDE_CALITATE
    "Ce standarde de calitate trebuie sa respecte studentii ASE?",
    "Cum se aplica standardele de calitate la ASE?",
    "Standarde calitate ASE",

    # UTILIZARE_FACILITATI
    "Cum pot studentii ASE sa utilizeze facilitatile universitare?",
    "Care sunt modalitatile de acces la facilitatile ASE pentru studenti?",
    "Facilitati ASE",

    # PRINCIPII_COD_ETICA
    "Care sunt principiile Codului de Etica in ASE?",
    "Ce obligatii etice sunt stipulate in Codul de Etica ASE?",
    "Cod etica ASE",

    # COOPERARE_COMUNITARA
    "Cum sunt subliniate cooperarea comunitara si atitudinea neconflictuala in codul etic al ASE?",
    "Ce principii de cooperare comunitara sunt promovate in ASE?",
    "Cooperare comunitara ASE",

    # NUMIRE_PRODECAN
    "Cum este numit Prodecanul in ASE si cine poate initia demiterea acestuia?",
    "Ce procedura urmeaza numirea Prodecanului in cadrul ASE?",
    "Numire Prodecan ASE",

    # SITUATII_DEMITERE_PRODECAN
    "Ce situatii pot duce la demiterea unui Prodecan in ASE?",
    "Care sunt cauzele care pot justifica revocarea unui Prodecan la ASE?",
    "Demitere Prodecan ASE"

    # SARCINI_STABILITE_PRODECAN
    "Ce sarcini are Prodecanul ASE?",
    "Atributii Prodecan ASE",
    "Responsabilitati Prodecan",

    # ADMITERE_PROGRAME_STUDII
    "Cum se face admiterea la ASE?",
    "Criterii admitere ASE",
    "Proces admitere studenti",

    # CALIFICARI_DOCUMENTE
    "Ce documente valideaza studiile ASE?",
    "Recunoastere diplome ASE",
    "Validare studii ASE",

    # STRUCTURA_AN_UNIVERSITAR
    "Cum sunt structurati anii universitari ASE?",
    "Organizare semestre ASE",
    "Calendar academic ASE",

    # TIPURI_PROGRAME_STUDII
    "Ce programe ofera ASE?",
    "Specializari disponibile ASE",
    "Nivele studiu ASE",

    # DURATA_MANDAT
    "Care este durata mandatului Prorector ASE?",
    "Termen mandat Prorector",
    "Perioada functiei Prorector",

    # CONDITII_DEMITERE_PRORECTOR
    "Ce conditii duc la demiterea Prorectorului?",
    "Cauze demitere Prorector",
    "Revocare Prorector conditii",

    # SARCINI_PRORECTOR
    "Ce sarcini are Prorectorul ASE?",
    "Atributii principale Prorector",
    "Roluri Prorector ASE",

    # ASIGURARE_CALITATE
    "Cum asigura Prorectorul calitatea la ASE?",
    "Monitorizare calitate ASE",
    "Strategii calitate educativa ASE",

    # ATRAGERE_FONDURI_EUROPENE
    "Cum atrage Prorectorul fonduri europene?",
    "Strategii accesare fonduri UE",
    "Gestionare parteneriate europene ASE",

    # ORGANIZARE_PROGRAM_STUDII
    "Cum sunt organizate programele de studii ASE?",
    "Planificare curriculara ASE",
    "Structurare cursuri ASE",

    # RELAȚII_INTERNAȚIONALE
    "Ce rol are Prorectorul in relatii internationale ASE?",
    "Strategii parteneriate internationale ASE",
    "Proiecte internationale ASE",

    # ATRIBUTII_RECTOR
    "Ce atributii are Rectorul ASE?",
    "Responsabilitati principale Rector",
    "Rol Rector in administratie ASE",

    # DESEMNARE_RECTOR
    "Cum este numit Rectorul ASE?",
    "Proces alegere Rector ASE",
    "Criterii selectie Rector",

    # DURATA_MANDAT_RECTOR
    "Ce durata are mandatul Rectorului ASE?",
    "Termen mandat Rector",
    "Numar mandate posibile Rector",

    # CONDITII_DEMITERE_RECTOR
    "Sub ce conditii poate fi demis Rectorul ASE?",
    "Proces demitere Rector",
    "Criterii revocare Rector"

    # CONTRIBUIE_CONDUCERE_OPERATIONALA
    "Cum contribuie Rectorul la conducerea ASE?",
    "Rolul Rectorului in deciziile operationale ASE",
    "Rectorul si conducerea ASE",

    # ASIGURARE_BUNA_DESFASURARE_CONCURSURI
    "Cum asigura Rectorul desfasurarea corecta a concursurilor?",
    "Rolul Rectorului in organizarea concursurilor",
    "Rector si concursuri",

    # ALEGERE_REPREZENTANTI_STUDENTI
    "Cum sunt alesi reprezentantii studentilor in structurile ASE?",
    "Procesul de alegere a reprezentantilor studentilor",
    "Alegere reprezentanti studenti",

    # DESEMNARE_MEMBRI_REPREZENTANTI
    "Cum sunt desemnati membrii reprezentanti ai studentilor?",
    "Regulile pentru desemnarea reprezentantilor studentilor",
    "Desemnare reprezentanti studenti",

    # PARTICIPARE_PROCES_DECIZIONAL
    "Cum participa studentii la procesul decizional in ASE?",
    "Influenta studentilor asupra deciziilor ASE",
    "Studenti si decizii ASE",

    # ROL_STUDENTI_DESEMNARE_RECTOR
    "Ce rol au studentii in desemnarea Rectorului?",
    "Cum influenteaza studentii alegerea Rectorului?",
    "Studenti si Rector",

    # REPREZENTANT_CONSILIU_ADMINISTRATIE
    "Cum este ales reprezentantul studentilor in Consiliul de Administratie?",
    "Procesul de selectie a reprezentantului studentilor in consiliu",
    "Reprezentant studenti consiliu",

    # APLICABIL_PERSONAL_DIDACTIC
    "Ce sanctiuni pot fi aplicate cadrelor didactice ASE?",
    "Regulile pentru sancționarea profesorilor ASE",
    "Sancțiuni profesori",

    # TIPURI_SANCTIUNI_PERSONAL_DIDACTIC
    "Ce tipuri de sanctiuni exista pentru cadrele didactice din ASE?",
    "Categorii de sanctiuni pentru profesori",
    "Sanctiuni cadre didactice",

    # TIPURI_SANCTIUNI_STUDENTI
    "Ce tipuri de sanctiuni pot fi aplicate studentilor ASE?",
    "Categorii de sanctiuni pentru studenti ASE",
    "Sanctiuni studenti",

    # ADOPTARE_REGULAMENT
    "Cand si cum se adopta regulamentul universitar ASE?",
    "Procesul de adoptare a regulamentului ASE",
    "Adoptare regulament",

    # ATRIBUTII_APROBARE_ACTIVITATI
    "Ce atributii are Senatul in aprobarea programelor ASE?",
    "Rolul Senatului in aprobarea activitatilor didactice si de cercetare",
    "Senat si programe",

    # STRUCTURA_SENATULUI
    "Cum este structurat Senatul Universitar ASE?",
    "Componentele Senatului Universitar ASE",
    "Structura Senat",

    # CONDITII_REPREZENTARE_STUDENTI
    "Ce conditii trebuie indeplinite pentru reprezentarea studentilor in Senat?",
    "Reguli pentru reprezentantii studentilor in Senat",
    "Studenti in Senat",

    # CONDUCERE_SENAT
    "Cum este condus Senatul Universitar ASE?",
    "Structura de conducere a Senatului Universitar",
    "Conducere Senat",

    # GARANTII_SENAT
    "Ce garanteaza Senatul Universitar pentru membrii sai?",
    "Asigurari oferite de Senatul Universitar",
    "Garantii Senat",

    # DURATA_MANDAT_SENAT
    "Ce durata are mandatul membrilor Senatului Universitar ASE?",
    "Termenul mandatului in Senatul Universitar",
    "Durata mandat Senat",

    # ORGANIZARE_SEDINTE
    "Cum se organizeaza sedintele Senatului Universitar ASE?",
    "Reguli pentru organizarea sedintelor Senatului",
    "Sedinte Senat",

    # VALORI_FUNDAMENTALE
    "Ce valori fundamentale promoveaza ASE?",
    "Valori fundamentale sustinute de ASE",
    "Valori ASE"  
    
# DEFINITIE_INTEGRITATE
    "Ce inseamna integritate pentru ASE?",
    "Cum defineste ASE integritatea?",
    "Integritate ASE",

    # PROFESIONALISM
    "Cum este vazut profesionalismul in ASE?",
    "Ce reprezinta profesionalismul pentru ASE?",
    "Profesionalism ASE",

    # ASIGURAREA_CALITATII
    "Cum este asigurata calitatea in ASE?",
    "Ce metode foloseste ASE pentru calitate?",
    "Calitate ASE",

    # AUTONOMIA_UNIVERSITARA
    "Ce inseamna autonomia universitara pentru ASE?",
    "Cum este aplicata autonomia universitara in ASE?",
    "Autonomie ASE",

    # CENTRAREA_EDUCATIEI_PE_STUDENT
    "Ce inseamna centrarea educatiei pe student in ASE?",
    "Cum promoveaza ASE centrarea pe student?",
    "Centrare student ASE",

    # EFICACITATEA_MANAGERIALA_SI_EFICIENTA_FINANCIARA
    "Ce inseamna eficacitatea manageriala si eficienta financiara pentru ASE?",
    "Cum masoara ASE eficacitatea manageriala?",
    "Eficacitate ASE",

    # INDEPENDENTA_FATA_DE_IDEOLOGII
    "Cum promoveaza ASE independenta fata de ideologii?",
    "Ce inseamna independenta de ideologii pentru ASE?",
    "Independenta ideologica ASE",

    # LIBERTATEA_ACADEMICA
    "Cum este sustinuta libertatea academica in ASE?",
    "Ce masuri sustin libertatea academica la ASE?",
    "Libertate academica ASE",

    # LIBERTATEA_DE_MOBILITATE
    "Ce inseamna libertatea de mobilitate pentru ASE?",
    "Cum este valorizata mobilitatea in ASE?",
    "Mobilitate ASE",

    # PARTENERIATUL_CU_ENTITATI
    "Cum contribuie parteneriatele cu entitati externe la ASE?",
    "Ce rol au parteneriatele cu entitati externe in ASE?",
    "Parteneriate externe ASE",

    # TRANSPARENTA_DECIZIONALA
    "Cum este asigurata transparenta decizionala in ASE?",
    "Ce masuri asigura transparenta in ASE?",
    "Transparenta ASE",

    # INTREBARI
    "Ce intrebari frecvente au studentii ASE?",
    "Ce tipuri de intrebari sunt comune in ASE?",
    "Intrebari ASE"
]

for question in questions:
    try:
        textarea = driver.find_element(By.NAME, 'question')
        textarea.clear()
        textarea.send_keys(question)

        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        time.sleep(2)

        print(f"Question: {question}\n")
    except Exception as e:
        print(f"Error processing question '{question}': {str(e)}")

# Infinite loop to keep the window open
while True:
    time.sleep(10)