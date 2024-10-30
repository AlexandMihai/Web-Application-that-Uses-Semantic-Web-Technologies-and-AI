from SPARQLWrapper import SPARQLWrapper, JSON
import re

entity_mapping = {
        "NIVEL_ACREDITARE": {
            "individual": "ASE",
            "property": "acreditare",
            "query_type": "base"
        },
        "CARACTER_UNIVERSITATE": {
            "individual": "ASE",
            "property": "character",
            "query_type": "base"
        },
        "DENUMIRE_OFICIALA": {
            "individual": "ASE",
            "property": "denumireOficiala",
            "query_type": "base"
        },
        "LOCATIE_SEDIU": {
            "individual": "ASE",
            "property": "sediu",
            "query_type": "base"
        },
        "SITE_WEB": {
            "individual": "ASE",
            "property": "siteWeb",
            "query_type": "base"
        },
        "DENUMIRE_ENGLEZA": {
            "individual": "ASE",
            "property": "denumireInEngleza",
            "query_type": "base"
        },
        "LEGE_INFIINTARE": {
            "individual": "ASE",
            "property": "infiintare",
            "query_type": "nodes",
            "node_properties": ["lege"]
        },
        "DECRET_REGAL": {
            "individual": "ASE",
            "property": "infiintare",
            "query_type": "nodes",
            "node_properties": ["decretRegal"]
        },
        "PROMULGATOR": {
            "individual": "ASE",
            "property": "infiintare",
            "query_type": "nodes",
            "node_properties": ["promulgator"]
        },

        "INFIINTARE_ASE": {
            "individual": "ASE",
            "property": "infiintare",
            "query_type": "nodes",
            "node_properties": ["decretRegal", "lege", "promulgator"]
        },

        "DATA_SARBATOARE": {
            "individual": "ASE",
            "property": "ziuaASE",
            "query_type": "base"
        },
        "TIP_DISCRIMINARE": {
            "individual": "AbateriEtice",
            "property": "discriminari",
            "query_type": "base"
        },
        "ABATERE_ETICA": {
            "individual": "AbateriEtice",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "ACTIVITATE_NENUMARATA": {
            "individual": "AbateriEtice",
            "property": "activitatiNeremunerateInFavoareaCadruDidactic",
            "query_type": "base"
        },
        "ABATERE_GRAVA": {
            "individual": "AbateriGrave",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "APROBATOR_SPATII": {
            "individual": "ActivitatiCulturaleEducativeSportive",
            "property": "aprobareSpatii",
            "query_type": "base"
        },
        "INCURAJARE_ACTIVITATI": {
            "individual": "ActivitatiCulturaleEducativeSportive",
            "property": "incourageazaActivitati",
            "query_type": "base"
        },
        "PLANIFICARE_EVENIMENTE": {
            "individual": "ActivitatiCulturaleEducativeSportive",
            "property": "organizareInAfara",
            "query_type": "base"
        },
        "TIP_EVENIMENTE": {
            "individual": "ActivitatiCulturaleEducativeSportive",
            "property": "organizareManifestari",
            "query_type": "base"
        },
        "PARTENERI_ORGANIZATII": {
            "individual": "ActivitatiCulturaleEducativeSportive",
            "property": "partenereOrganizatii",
            "query_type": "base"
        },
        "RESPONSABIL_ORGANIZARE": {
            "individual": "ActivitatiCulturaleEducativeSportive",
            "property": "responsabilitateOrganizare",
            "query_type": "base"
        },
        "SUSTINERE_ACTIVITATI": {
            "individual": "ActivitatiCulturaleEducativeSportive",
            "property": "sustinereFinanciara",
            "query_type": "base"
        },
        "RATIFICATOR_CARTE": {
            "individual": "AmendareAprobareCarta",
            "property": "aprobare",
            "query_type": "base"
        },
        "INITIATOR_AMENDA": {
            "individual": "AmendareAprobareCarta",
            "property": "initiativaAmendare",
            "query_type": "base"
        },
        "EXECUTOR_SANCTIUNI": {
            "individual": "AplicareSancțiuniRector",
            "property": "executor",
            "query_type": "base"
        },
        "TERMEN_SANCTIUNI": {
            "individual": "AplicareSancțiuniRector",
            "property": "termenAplicare",
            "query_type": "base"
        },
        "AUTONOMIE_DIDACTICA": {
            "individual": "AutonomiaUniversitară",
            "property": "autonomieDidactică",
            "query_type": "nodes",
            "node_properties": ["conținutProgramStudii", "managementActivitățiPredare", "standardeEvaluareCalitate",
                                "înființareReorganizareDesființareFacultăți"]
        },
        "AUTONOMIE_FINANCIARA": {
            "individual": "AutonomiaUniversitară",
            "property": "autonomieFinanciară",
            "query_type": "nodes",
            "node_properties": ["acceptareDonații", "constituireUnitățiGeneratoareVenit", "elaborareBuget",
                                "modulAdministrareSpațiu", "obținereResurseProprii", "utilizareResurseTransparent"]
        },
        "AUTONOMIE_FUNCTIONALA": {
            "individual": "AutonomiaUniversitară",
            "property": "autonomieFuncțională",
            "query_type": "nodes",
            "node_properties": ["facilitareMobilitate", "inițiereParteneriate", "publicareMaterialeȘtiințifice",
                                "realizareActivitățiLegale", "stabilirePlanuriÎnvățământ",
                                "înființareStructuriOrganizatorice"]
        },
        "CHELTUIELI_LEGE": {
            "individual": "CheltuieliSiGestionareResurseASE",
            "property": "cheltuieliCuRespectareaLegii",
            "query_type": "base"
        },
        "DEZVOLTARE_BAZA_MATERIALA": {
            "individual": "CheltuieliSiGestionareResurseASE",
            "property": "constituireDezvoltareInstrainareBazaMateriala",
            "query_type": "base"
        },
        "PRINCIPII_GESTIONARE": {
            "individual": "CheltuieliSiGestionareResurseASE",
            "property": "principiuPrudentialitateTransparenta",
            "query_type": "base"
        },
        "UTILIZARE_SPONSORIZARI": {
            "individual": "CheltuieliSiGestionareResurseASE",
            "property": "utilizareResurseSponsorizariConformContract",
            "query_type": "base"
        },
        "MINIMIZARE_HARTUIRE": {
            "individual": "ComisiaConfidențialitate",
            "property": "minimizareTeamaHărțuireSexuală",
            "query_type": "base"
        },
        "MOD_SOLUTIE": {
            "individual": "ComisiaConfidențialitate",
            "property": "modSoluționare",
            "query_type": "base"
        },
        "PROTEJARE_IDENTITATE": {
            "individual": "ComisiaConfidențialitate",
            "property": "protejareIdentitateVictime",
            "query_type": "base"
        },
        "ATRIBUTII_COMISIA_ETICA": {
            "individual": "ComisiaDeEtica",
            "property": "atributii",
            "query_type": "base"
        },
        "COMPOZITIE_COMISIA_ETICA": {
            "individual": "ComisiaDeEtica",
            "property": "compozitie",
            "query_type": "base"
        },
        "CONSTITUIRE_COMISIA_ETICA": {
            "individual": "ComisiaDeEtica",
            "property": "constituire",
            "query_type": "base"
        },
        "EXCLUDERE_COMISIA_ETICA": {
            "individual": "ComisiaDeEtica",
            "property": "excludere",
            "query_type": "base"
        },
        "HOTARARI_COMISIA_ETICA": {
            "individual": "ComisiaDeEtica",
            "property": "hotarari",
            "query_type": "base"
        },
        "CALITATE_CERCETATOR_POSTDOCTORAT": {
            "individual": "ComunitateaUniversitară",
            "property": "calitateCercetătorPostdoctorat",
            "query_type": "base"
        },
        "CALITATE_CURSANT": {
            "individual": "ComunitateaUniversitară",
            "property": "calitateCursant",
            "query_type": "base"
        },
        "CALITATE_PERSONAL_DIDACTIC": {
            "individual": "ComunitateaUniversitară",
            "property": "calitatePersonalDidactic",
            "query_type": "base"
        },
        "CALITATE_STUDENTI": {
            "individual": "ComunitateaUniversitară",
            "property": "calitateStudenți",
            "query_type": "base"
        },
        "ATRIBUTII_PERSONAL": {
            "individual": "ComunitateaUniversitară",
            "property": "atribuțiiPersonal",
            "query_type": "base"
        },
        "COLABORARE_VIZIUNE_MISIUNE": {
            "individual": "ComunitateaUniversitară",
            "property": "colaborareViziuneMisiuneObiective",
            "query_type": "base"
        },
        "DIALOG_SOCIAL": {
            "individual": "ComunitateaUniversitară",
            "property": "dialogSocial",
            "query_type": "base"
        },
        "EQUIVALARE_FUNCTII": {
            "individual": "ComunitateaUniversitară",
            "property": "echivalareFuncții",
            "query_type": "base"
        },
        "STRUCTURARE_COMUNITATE": {
            "individual": "ComunitateaUniversitară",
            "property": "structurare",
            "query_type": "nodes",
            "node_properties": ["cercetătoriPostdoctorat", "cursanți", "personalDidactic", "personalDidacticAuxiliar",
                                "studenți"]
        },
        "STRUCTURA_CERCETATORI_POSTDOCTORAT": {
            "individual": "ComunitateaUniversitară",
            "property": "cercetătoriPostdoctorat",
            "query_type": "base"
        },
        "STRUCTURA_CURSANTI": {
            "individual": "ComunitateaUniversitară",
            "property": "cursanți",
            "query_type": "base"
        },
        "STRUCTURA_PERSONAL_DIDACTIC": {
            "individual": "ComunitateaUniversitară",
            "property": "personalDidactic",
            "query_type": "base"
        },
        "STRUCTURA_PERSONAL_DIDACTIC_AUXILIAR": {
            "individual": "ComunitateaUniversitară",
            "property": "personalDidacticAuxiliar",
            "query_type": "base"
        },
        "STRUCTURA_STUDENTI": {
            "individual": "ComunitateaUniversitară",
            "property": "studenți",
            "query_type": "base"
        },
        "CONFLICT_INTERESE_DECIZII_ACTE": {
            "individual": "ConflictDeInterese",
            "property": "deciziiSauActe",
            "query_type": "base"
        },
        "INCOMPATIBILITATI_CONFLICT_INTERESE": {
            "individual": "ConflictDeInterese",
            "property": "incompatibilitati",
            "query_type": "base"
        },
        "INFLUENTA_INDEPLINIRE_ATRIBUTII": {
            "individual": "ConflictDeInterese",
            "property": "influenta",
            "query_type": "base"
        },
        "INTERES_PERSONAL": {
            "individual": "ConflictDeInterese",
            "property": "interesPersonal",
            "query_type": "base"
        },
        "OBLIGATIE_INFORMARE": {
            "individual": "ConflictDeInterese",
            "property": "obligatieInformare",
            "query_type": "base"
        },
        "SITUATIE_CONFLICT": {
            "individual": "ConflictDeInterese",
            "property": "situatie",
            "query_type": "base"
        },
        "VERIFICARE_CONFLICT": {
            "individual": "ConflictDeInterese",
            "property": "verificare",
            "query_type": "base"
        },
        "ANALIZA_PLANURI_INVATAMANT": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "analizaPlanuriInvatamant",
            "query_type": "base"
        },
        "APROBARE_CERERI_CONCEDII": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "aprobareCereriConcedii",
            "query_type": "base"
        },
        "APROBARE_CONCURS_POSTURI": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "aprobareConcursPosturi",
            "query_type": "base"
        },
        "APROBARE_OPERATIUNI_FINANCIARE": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "aprobareOperatiuniFinanciare",
            "query_type": "base"
        },
        "AVIZARE_EXAMEN_MEDICAL": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "avizareExamenMedical",
            "query_type": "base"
        },
        "AVIZARE_RAPORT_REGIE": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "avizareRaportRegie",
            "query_type": "base"
        },
        "ELABORARE_BUGET_BILANT": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "elaborareBugetBilant",
            "query_type": "base"
        },
        "ELABORARE_REGULAMENTE_METODOLOGII": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "elaborareRegulamenteMetodologii",
            "query_type": "nodes",
            "node_properties": [
                "admitere",
                "alteAspecteActivitati",
                "conferireaTitlurilorDistinctii",
                "cooperareInternationala",
                "cuantificareOreConventii",
                "evaluarePeriodicaPersonalDidactic",
                "ocupareaPosturiDidacticeCercetare",
                "organizareFunctionareStructuri",
                "recunoastereEchivalareStudii",
                "sanctionarePersonalPerformanteSlabe",
                "taxePerceptie"
            ]
        },
        "INDEPLINIRE_ALTE_ATRIBUTII": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "indeplinireAlteAtributii",
            "query_type": "base"
        },
        "ORGANIZARE_CONCURS_DIRECTOR": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "organizareConcursDirector",
            "query_type": "base"
        },
        "PROPUNERE_AN_SABATIC": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "propunereAnSabatic",
            "query_type": "base"
        },
        "PROPUNERE_COMISIE_ETICA": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "propunereComisieEtica",
            "query_type": "base"
        },
        "STABILIRE_PARTENERIATE": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "stabilireParteneriate",
            "query_type": "base"
        },
        "VALIDARE_COMISIE_CONCURS": {
            "individual": "ConsiliulDeAdministratieAtributii",
            "property": "validareComisieConcurs",
            "query_type": "base"
        },
        "ALEGERI_CONSILIUL_DEPARTAMENTULUI": {
            "individual": "ConsiliulDepartamentului",
            "property": "alegeri",
            "query_type": "base"
        },
        "REGULAMENT_CONSILIUL_DEPARTAMENTULUI": {
            "individual": "ConsiliulDepartamentului",
            "property": "regulamentPropriu",
            "query_type": "base"
        },
        "ALEGERI_CONSILIUL_FACULTATII": {
            "individual": "ConsiliulFacultatii",
            "property": "alegeri",
            "query_type": "base"
        },
        "ATRIBUTII_CONSILIUL_FACULTATII": {
            "individual": "ConsiliulFacultatii",
            "property": "atributii",
            "query_type": "nodes",
            "node_properties": ["propunereStrategii"]
        },
        "COMPOZITIE_CONSILIUL_FACULTATII": {
            "individual": "ConsiliulFacultatii",
            "property": "compozitie",
            "query_type": "nodes",
            "node_properties": ["reprezentantiPersonalDidactic", "reprezentantiStudenti"]
        },
        "CONDITII_MEMBRI_PERSONAL_DIDACTIC": {
            "individual": "ConsiliulFacultatii",
            "property": "conditiiMembriPersonalDidactic",
            "query_type": "base"
        },
        "CONDITII_MEMBRI_STUDENTI": {
            "individual": "ConsiliulFacultatii",
            "property": "conditiiMembriStudenti",
            "query_type": "base"
        },
        "QUORUM_CONSILIUL_FACULTATII": {
            "individual": "ConsiliulFacultatii",
            "property": "quorum",
            "query_type": "base"
        },
        "SEDINTE_CONDUCERE_CONSILIUL_FACULTATII": {
            "individual": "ConsiliulFacultatii",
            "property": "sedinteConducere",
            "query_type": "base"
        },
        "SEDINTE_FRECVENTA_CONSILIUL_FACULTATII": {
            "individual": "ConsiliulFacultatii",
            "property": "sedinteFrecventa",
            "query_type": "base"
        },
        "VOT_CONSILIUL_FACULTATII": {
            "individual": "ConsiliulFacultatii",
            "property": "votMajoritate",
            "query_type": "base"
        },
        "ALEGERI_CONSILIUL_SCOLII_DOCTORALE": {
            "individual": "ConsiliulScoliiDoctorale",
            "property": "alegeri",
            "query_type": "base"
        },
        "REGULAMENT_CONSILIUL_SCOLII_DOCTORALE": {
            "individual": "ConsiliulScoliiDoctorale",
            "property": "regulamentPropriu",
            "query_type": "base"
        },
        "ATRIBUTII_C_S_U_DOCTORAT": {
            "individual": "ConsiliulStudiiUniversitareDoctorat",
            "property": "atributii",
            "query_type": "nodes",
            "node_properties": [
                "atributiiSpecifice",
                "coordonareParteneriate",
                "elaborareRegulamentDoctorat",
                "propunereInfiintareReorganizare",
                "selectareConducatoriDoctorat"
            ]
        },
        "COORDONARE_PARTENERIATE": {
            "individual": "ConsiliulStudiiUniversitareDoctorat",
            "property": "coordonareParteneriate",
            "query_type": "base"
        },
        "CONDITII_MEMBRI_CADRE_DIDACTICE": {
            "individual": "ConsiliulStudiiUniversitareDoctorat",
            "property": "conditiiMembriCadreDidactice",
            "query_type": "base"
        },
        "DESEMNARE_DIRECTOR": {
            "individual": "ConsiliulStudiiUniversitareDoctorat",
            "property": "director",
            "query_type": "nodes",
            "node_properties": ["desemnare", "functieAsimilata"]
        },
        "MANDAT_CADRE_DIDACTICE": {
            "individual": "ConsiliulStudiiUniversitareDoctorat",
            "property": "mandatCadreDidactice",
            "query_type": "base"
        },
        "NUMAR_MEMBRI": {
            "individual": "ConsiliulStudiiUniversitareDoctorat",
            "property": "numarMembri",
            "query_type": "base"
        },
        "DATA_APROBARE": {
            "individual": "DateAprobareModificare",
            "property": "dataAprobare",
            "query_type": "base"
        },
        "DATA_MODIFICARE": {
            "individual": "DateAprobareModificare",
            "property": "dataModificare",
            "query_type": "base"
        },
        "VIGOARE": {
            "individual": "DateAprobareModificare",
            "property": "vigoare",
            "query_type": "base"
        },
        "MEMBRU_DREPT_CONSILIU_ADMINISTRATIE": {
            "individual": "Decan",
            "property": "membruDeDreptConsiliulAdministratie",
            "query_type": "base"
        },
        "SITUATII_DEMISIE_DECAN": {
            "individual": "Decan",
            "property": "poateFiiDemis",
            "query_type": "nodes",
            "node_properties": [
                "de",
                "situatii"
            ]
        },
        "RESPONSABILITATI_MANAGEMENT_FACULTATE": {
            "individual": "Decan",
            "property": "responsabilManagementFacultate",
            "query_type": "base"
        },
        "SARCINI_DECAN": {
            "individual": "Decan",
            "property": "sarcini",
            "query_type": "nodes",
            "node_properties": [
                "anulareRezultatEvaluare",
                "aplicareHotarari",
                "avizeazaFisaPostului",
                "conducereSedinteConsiliulFacultatii",
                "indeplinesteSarciniStabilite",
                "numireProdecani",
                "prezintaRapoarteConsiliuAdministratie",
                "prezintaRapoarteConsiliuFacultate",
                "propuneSancțiuniDisciplinare",
                "publicaDecizii",
                "raspundeAngajareEvaluarePersonal",
                "raspundeConcursuriOcuparePosturi",
                "raspundeManagementCalitateFinanciar",
                "semneazaActeDiplome"
            ]
        },
        "SELECTIE_DECAN": {
            "individual": "Decan",
            "property": "selectie",
            "query_type": "base"
        },
        "ASUMARE_OBLIGATII_DEONTOLOGIA": {
            "individual": "DeontologiaUniversitară",
            "property": "asumareObligații",
            "query_type": "base"
        },
        "DEMNITATE_CONDUITA_DEONTOLOGIA": {
            "individual": "DeontologiaUniversitară",
            "property": "demnitateȘiConduită",
            "query_type": "base"
        },
        "PRODUCEREA_CUNOASTERII": {
            "individual": "DepartamentUnitateAcademica",
            "property": "asiguraProducereaCunoasterii",
            "query_type": "base"
        },
        "CONDUCERE_DEPARTAMENT": {
            "individual": "DepartamentUnitateAcademica",
            "property": "conducere",
            "query_type": "base"
        },
        "INFIINTARE_DEPARTAMENT": {
            "individual": "DepartamentUnitateAcademica",
            "property": "infiintare",
            "query_type": "base"
        },
        "STRUCTURA_DEPARTAMENT": {
            "individual": "DepartamentUnitateAcademica",
            "property": "structura",
            "query_type": "nodes",
            "node_properties": [
                "centreCercetare",
                "centreConsultanta",
                "laboratoare",
                "scoliPostuniversitare"
            ]
        },
        "FUNCTIE_DIRECTOR_CSUD": {
            "individual": "DirectorCSUD",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "CONDUCE_COMPONENTE": {
            "individual": "DirectorGeneralAdjunctAdministrativ",
            "property": "conduceComponenteStructuraAdministrativa",
            "query_type": "base"
        },
        "SUBORDONAT_DIRECTOR_GENERAL": {
            "individual": "DirectorGeneralAdjunctAdministrativ",
            "property": "subordonat",
            "query_type": "base"
        },
        "CONDUCE_STRUCTURA_ADMINISTRATIVA": {
            "individual": "DirectorGeneralAdministrativ",
            "property": "conduceStructuraAdministrativaASE",
            "query_type": "base"
        },
        "OCUPARE_POST_DIRECTOR_GENERAL": {
            "individual": "DirectorGeneralAdministrativ",
            "property": "ocuparePost",
            "query_type": "base"
        },
        "SITUATII_DEMISIE_DIRECTOR_GENERAL": {
            "individual": "DirectorGeneralAdministrativ",
            "property": "poateFiiDemis",
            "query_type": "nodes",
            "node_properties": [
                "de",
                "situatii"
            ]
        },
        "RESPONSABILITATI_GESTIONARE_ECONOMICO_FINANCIARA": {
            "individual": "DirectorGeneralAdministrativ",
            "property": "responsabilGestionareEconomicoFinanciara",
            "query_type": "base"
        },
        "CONDUCERE_OPERATIVA_DEPARTAMENT": {
            "individual": "DirectorulDeDepartament",
            "property": "asiguraConducereOperativa",
            "query_type": "base"
        },
        "REVOCARE_DIRECTOR_DEPARTAMENT": {
            "individual": "DirectorulDeDepartament",
            "property": "poateFiiRevocat",
            "query_type": "nodes",
            "node_properties": [
                "de",
                "situatii"
            ]
        },
        "SARCINI_DIRECTOR_DEPARTAMENT": {
        "individual": "DirectorulDeDepartament",
        "property": "sarcini",
        "query_type": "nodes",
        "node_properties": [
            "avizeazaCereriAnSabatic",
            "contribuiePlanuriDeInvatamant",
            "coordoneazaCercetare",
            "elaboreazaStateDeFunctii",
            "imbunatatesteEducatieCercetare",
            "indeplinesteSarciniFisaPostului",
            "intocmesteFiseDePost",
            "organizeazaSelectieEvaluarePersonal",
            "propuneNormeDidactice",
            "propunePosturiDidactice",
            "raspundeManagementCalitateFinanciar",
            "raspundeOrganizareConcursuri"
        ]
        },
        "SELECTIE_DIRECTOR_DEPARTAMENT": {
            "individual": "DirectorulDeDepartament",
            "property": "selectie",
            "query_type": "base"
        },
        "CONDUCERE_OPERATIVA_SCOLI_DOCTORALE": {
            "individual": "DirectorulScoliiDoctorale",
            "property": "asiguraConducereOperativa",
            "query_type": "base"
        },
        "REVOCARE_DIRECTOR_SCOLI_DOCTORALE": {
            "individual": "DirectorulScoliiDoctorale",
            "property": "poateFiiRevocat",
            "query_type": "nested_nodes",
            "node_properties": [
                {
                    "name": "de",
                    "type": "simple"
                },
                {
                    "name": "situatii",
                    "type": "nested",
                    "properties": [
                        {"name": "cerereMajoritateSimpleConducatoriDoctorat", "type": "simple"},
                        {"name": "incalcareCodEticaDeontologie", "type": "simple"},
                        {"name": "incalcareIndatoririStandardePerformanta", "type": "simple"},
                        {"name": "incompatibilitateLegal", "type": "simple"},
                        {"name": "prejudiciuInteresePrestigiuASE", "type": "simple"}
                    ]
                }
            ]
        },
        "SARCINI_DIRECTOR_SCOLI_DOCTORALE": {
            "individual": "DirectorulScoliiDoctorale",
            "property": "sarcini",
            "query_type": "nodes",
            "node_properties": [
                "asiguraAutoevaluarePeriodica",
                "asistaEvaluatoriEvaluareExternaInterna",
                "avizeazaComisiiSustinerePublicaTeze",
                "coordoneazaEvaluareDosareAbilitare",
                "coordoneazaPropuneriInmatriculareExmatriculare",
                "coordoneazaPropuneriIntreruperePrelungireProgram",
                "coordoneazaRegulamentScoalaDoctorala",
                "decideSchimbareConducatorDoctorat",
                "raspundeAcordareCalitateMembru",
                "raspundeRevocareCalitateMembru",
                "reprezintaScoalaDoctorala"
            ]
        },
        "SELECTIE_DIRECTOR_SCOLI_DOCTORALE": {
            "individual": "DirectorulScoliiDoctorale",
            "property": "selectie",
            "query_type": "base"
        },
        "DREPTURI_PERSONAL_DIDACTIC_CERCETARE": {
            "individual": "DrepturileSiObligatiilePersonaluluiDidacticSiDeCercetare",
            "property": "drepturi",
            "query_type": "nodes",
            "node_properties": [
                "alegereSiAlegereInStructuri",
                "candidareGranturi",
                "concediiCuPlata",
                "concediiFaraPlata",
                "concediuOdihna",
                "exprimareLiberaOpinii",
                "mobilitateInternationala",
                "parteDinAsociatii",
                "participareConcursPublicConducere",
                "participareGradatieMerit",
                "proprietateIntelectuala",
                "protectieSpatiuUniversitar",
                "publicareSiEditare",
                "remuneratieMunca",
                "rezervarePostului"
            ]
        },
        "OBLIGATII_PERSONAL_DIDACTIC_CERCETARE": {
            "individual": "DrepturileSiObligatiilePersonaluluiDidacticSiDeCercetare",
            "property": "obligatii",
            "query_type": "nodes",
            "node_properties": [
                "activitateDidacticaCercetareCalitate",
                "contribuireMisiuneASE",
                "controlMedicalPeriodic",
                "evaluarePeriodica",
                "indeplinireSarciniContract",
                "respectareCodEticaDeontologie",
                "respectareDeontologieOriginalitate"
            ]
        },
        "EXPRIMARE_LIBERA_OPINII": {
            "individual": "DrepturileSiObligatiilePersonaluluiDidacticSiDeCercetare",
            "property": "exprimareLiberaOpinii",
            "query_type": "base"
        },
        "MOBILITATE_INTERNATIONALA": {
            "individual": "DrepturileSiObligatiilePersonaluluiDidacticSiDeCercetare",
            "property": "mobilitateInternationala",
            "query_type": "base"
        },
        "CONCEDIILE_CU_FARA_PLATA": {
            "individual": "DrepturileSiObligatiilePersonaluluiDidacticSiDeCercetare",
            "property": "drepturi",
            "query_type": "nodes",
            "node_properties": [
                "concediiCuPlata",
                "concediiFaraPlata"
            ]
        },
        "PROTECTIE_SPATIU_UNIVERSITAR": {
            "individual": "DrepturileSiObligatiilePersonaluluiDidacticSiDeCercetare",
            "property": "protectieSpatiuUniversitar",
            "query_type": "base"
        },
        "EVALUARE_PERIODICA": {
            "individual": "DrepturileSiObligatiilePersonaluluiDidacticSiDeCercetare",
            "property": "obligatii",
            "query_type": "nodes",
            "node_properties": [
                "evaluarePeriodica"
            ]
        },
        "CONTRIBUIRE_MISIUNE_ASE": {
            "individual": "DrepturileSiObligatiilePersonaluluiDidacticSiDeCercetare",
            "property": "obligatii",
            "query_type": "nodes",
            "node_properties": [
                "contribuireMisiuneASE"
            ]
        },
        "ACCES_HOTARARI": {
            "individual": "DrepturileStudentilor",
            "property": "accesHotarari",
            "query_type": "base"
        },
        "BENEFICIERE_ASISTENTA_MEDICALA": {
            "individual": "DrepturileStudentilor",
            "property": "beneficiereAsistentaMedicala",
            "query_type": "base"
        },
        "BENEFICIERE_CAZARE": {
            "individual": "DrepturileStudentilor",
            "property": "beneficiereCazare",
            "query_type": "base"
        },
        "BENEFICIERE_PROTECTIE_UNIVERSITAR": {
            "individual": "DrepturileStudentilor",
            "property": "beneficiereProtectieUniversitar",
            "query_type": "base"
        },
        "BENEFICIERE_SERVICII": {
            "individual": "DrepturileStudentilor",
            "property": "beneficiereServicii",
            "query_type": "base"
        },
        "CONTESTARE_NOTE": {
            "individual": "DrepturileStudentilor",
            "property": "contestareNote",
            "query_type": "base"
        },
        "PROPRIETATE_INTELECTUALA": {
            "individual": "DrepturileStudentilor",
            "property": "proprietateIntelectuala",
            "query_type": "base"
        },
        "DESFASURARE_ACTIUNI": {
            "individual": "DrepturileStudentilor",
            "property": "desfasurareActiuni",
            "query_type": "base"
        },
        "LIMITARE_ORAR": {
            "individual": "DrepturileStudentilor",
            "property": "limitareOrar",
            "query_type": "base"
        },
        "PARTICIPARE_PROCES_ELABORARE_REGULAMENTE": {
            "individual": "DrepturileStudentilor",
            "property": "participareProcesElaborareRegulamente",
            "query_type": "base"
        },
        "RECUNOASTERE_PRACTICA_INDIVIDUALA": {
            "individual": "DrepturileStudentilor",
            "property": "recunoasterePracticaIndividuala",
            "query_type": "base"
        },
        "PROTECTIE_DATE_PERSONALE": {
            "individual": "DrepturileStudentilor",
            "property": "protectieDatePersonale",
            "query_type": "base"
        },
        "STUDIU_LIMBA_INTERNATIONALA": {
            "individual": "DrepturileStudentilor",
            "property": "studiuLimbaInternationala",
            "query_type": "base"
        },
        "SESIZARE_ABUZURI": {
            "individual": "DrepturileStudentilor",
            "property": "sesizareAbuzuri",
            "query_type": "base"
        },
        "TERMENE_INSCRIERE": {
            "individual": "DrepturileStudentilor",
            "property": "termeneInscriere",
            "query_type": "base"
        },
        "UTILIZARE_FACILITATI": {
            "individual": "DrepturileStudentilor",
            "property": "utilizareFacilitati",
            "query_type": "base"
        },
        "STUDII_GRATUITE_CENTRE_PLASAMENT": {
            "individual": "DrepturileStudentilorCentrePlasament",
            "property": "studiiGratuite",
            "query_type": "base"
        },
        "ACCES_ADAPTAT_DIZABILITATI": {
            "individual": "DrepturileStudentilorCuDizabilitati",
            "property": "accesAdaptat",
            "query_type": "base"
        },
        "CONDITII_NORMALE_DIZABILITATI": {
            "individual": "DrepturileStudentilorCuDizabilitati",
            "property": "conditiiNormale",
            "query_type": "base"
        },
        "BENEFICIERE_LOGISTICA_DOCTORAT": {
            "individual": "DrepturileStudentilorDoctorat",
            "property": "beneficiereLogistica",
            "query_type": "base"
        },
        "COLABORARE_ECHIPE_CERCETARE": {
            "individual": "DrepturileStudentilorDoctorat",
            "property": "colaborareEchipe",
            "query_type": "base"
        },
        "MOBILITATI_DOCTORAT": {
            "individual": "DrepturileStudentilorDoctorat",
            "property": "mobilitati",
            "query_type": "base"
        },
        "REPREZENTARE_FORURI_DOCTORAT": {
            "individual": "DrepturileStudentilorDoctorat",
            "property": "reprezentareForuri",
            "query_type": "base"
        },
        "GRATUITATE_MANIFESTARI_ROMANI": {
            "individual": "DrepturileStudentilorEtniciRomani",
            "property": "gratuitateManifestari",
            "query_type": "base"
        },
        "LOCURI_FINANTATE_MARGINALIZATI": {
            "individual": "DrepturileStudentilorMarginalizati",
            "property": "locuriFinantate",
            "query_type": "base"
        },
        "SERVICII_URMARIRE_MARGINALIZATI": {
            "individual": "DrepturileStudentilorMarginalizati",
            "property": "serviciiUrmărire",
            "query_type": "base"
        },
        "EVIDENTA_STUDENTI": {
            "individual": "FacultateUnitateFunctionala",
            "property": "evidențăStudenți",
            "query_type": "base"
        },
        "DEFINITIE_FACULTATE": {
            "individual": "FacultateUnitateFunctionala",
            "property": "facultate",
            "query_type": "base"
        },
        "ORGANISM_DECIZIONAL_FACULTATE": {
            "individual": "FacultateUnitateFunctionala",
            "property": "organismDecizional",
            "query_type": "base"
        },
        "STRUCTURA_FACULTATE": {
            "individual": "FacultateUnitateFunctionala",
            "property": "structuraFacultate",
            "query_type": "nodes",
            "node_properties": ["departamente", "extensiiUniversitare", "școliDoctorale", "școliPostuniversitare"]
        },
        "INFIINTARE_FUNCTIONARE_DESFIINTARE_FACULTATE": {
            "individual": "FacultateUnitateFunctionala",
            "property": "înființareFuncționareȘiDesființare",
            "query_type": "base"
        },
        "CONTRACTE_MINISTER_RESORT": {
            "individual": "FinantareaSiVenituriASE",
            "property": "contracteMinisterulResort",
            "query_type": "base"
        },
        "FINANTARE_ALTE_SURSE": {
            "individual": "FinantareaSiVenituriASE",
            "property": "finantareAlteMinistereImprumuturiSurseExterne",
            "query_type": "base"
        },
        "FINANTARE_CERCETARE_STIINTIFICA": {
            "individual": "FinantareaSiVenituriASE",
            "property": "finantareCercetareStiintifica",
            "query_type": "base"
        },
        "FINANTARE_TAXE_SCOLARIZARE": {
            "individual": "FinantareaSiVenituriASE",
            "property": "finantareTaxeScolarizarePrestatiiUniversitare",
            "query_type": "base"
        },
        "VENITURI_PROPRII": {
            "individual": "FinantareaSiVenituriASE",
            "property": "venituriProprii",
            "query_type": "base"
        },
        "CONFLICT_INTERESE_SITUATII": {
            "individual": "IncompatibilityReporting",
            "property": "conflictInterese",
            "query_type": "nodes",
            "node_properties": [
                "detinereFunctieConducereContracteComerciale", "influentaDeciziiInteresePatrimoniale",
                "participareComisiiAcelasiOrgan", "relatiiAfiniRude", "relatiiCaracterPatrimonial"
            ]
        },
        "INFORMARE_CONFLICT": {
            "individual": "IncompatibilityReporting",
            "property": "informare",
            "query_type": "base"
        },
        "REZOLVARE_INCOMPATIBILITATE": {
            "individual": "IncompatibilityReporting",
            "property": "rezolvareIncompatibilitate",
            "query_type": "base"
        },
        "MANIFESTARE_LIBERTATE_ACADEMICA": {
            "individual": "LibertateaAcademica",
            "property": "manifestare",
            "query_type": "nodes",
            "node_properties": [
                "accesSpațiuUniversitar",
                "dreptAsociere",
                "dreptCercetareTematică",
                "dreptConsultanță",
                "dreptExprimareOpinii",
                "dreptProducereDobândireDezvoltare",
                "dreptSelectareMembri"
            ]
        },
        "PERMISE_ACTIVITATI": {
            "individual": "LibertateaAcademica",
            "property": "permiseActivități",
            "query_type": "base"
        },
        "PRINCIPII_MANAGEMENT_CALITATE": {
            "individual": "ManagementulCalitatiiUniversitare",
            "query_type": "all_properties",
            "filterCondition": "FILTER(STRSTARTS(STR(?property), STR(ase:)))"
        },
        "EVALUARE_ACTIVITATE_DIDACTICA_STIINTIFICA": {
            "individual": "ManagementulCalitatiiUniversitare",
            "property": "evaluareActivitateDidacticaStiintifica",
            "query_type": "base"
        },
        "PROCEDURI_EVALUARE_CALITATE": {
            "individual": "ManagementulCalitatiiUniversitare",
            "property": "proceduriEvaluareCalitate",
            "query_type": "base"
        },
        "STUDENTI_IMPLICARE_MANAGEMENT": {
            "individual": "MembriiComunitatiiUniversitare",
            "property": "studentiDrepturiDepline",
            "query_type": "base"
        },
        "MISIUNE_CERCETARE": {
            "individual": "Misiune",
            "property": "misiuneDeCercetare",
            "query_type": "base"
        },
        "MISIUNE_EDUCATIONALA": {
            "individual": "Misiune",
            "property": "misiuneEducationala",
            "query_type": "base"
        },
        "MISIUNE_COMUNITATE": {
            "individual": "Misiune",
            "property": "misiunePentruComunitate",
            "query_type": "base"
        },
        "OBLIGATII_FINANCIARE_STUDENTI": {
            "individual": "ObligatiileStudentilor",
            "property": "achitareObligatii",
            "query_type": "base"
        },
        "COMPORTAMENT_CIVIC": {
            "individual": "ObligatiileStudentilor",
            "property": "comportamentCivic",
            "query_type": "base"
        },
        "RESPECTARE_CURATENIE_ORDINE": {
            "individual": "ObligatiileStudentilor",
            "property": "respectareCuratenie",
            "query_type": "base"
        },
        "RESPECTARE_STANDARDE_CALITATE": {
            "individual": "ObligatiileStudentilor",
            "property": "respectareStandarde",
            "query_type": "base"
        },
        "UTILIZARE_FACILITATI": {
            "individual": "ObligatiileStudentilor",
            "property": "utilizareFacilitati",
            "query_type": "base"
        },
        "OBLIGATIE_CONDUCATOR_DOCTORAT": {
            "individual": "ObligatiileStudentilorDoctorat",
            "property": "fieLegaturaPermanenta",
            "query_type": "base"
        },
        "PREZENTARE_RAPOARTE": {
            "individual": "ObligatiileStudentilorDoctorat",
            "property": "prezentareRapoarte",
            "query_type": "base"
        },
        "RESPECTARE_DISCIPLINA": {
            "individual": "ObligatiileStudentilorDoctorat",
            "property": "respectareDisciplina",
            "query_type": "base"
        },
        "RESPECTARE_PROGRAM_PREGATIRE": {
            "individual": "ObligatiileStudentilorDoctorat",
            "property": "respectareProgramPregatire",
            "query_type": "base"
        },
        "GESTIONARE_PATRIMONIU": {
            "individual": "PatrimoniuASE",
            "property": "aprobareCuantumStructuraAport",
            "query_type": "base"
        },
        "INCHIRIERE_ACTIVE_PATRIMONIALE": {
            "individual": "PatrimoniuASE",
            "property": "inchiriereActivePatrimoniale",
            "query_type": "base"
        },
        "PARTICIPARE_FUNDATII_ASOCIATII": {
            "individual": "PatrimoniuASE",
            "property": "participareFundatiiAsociatiiSocietatiComerciale",
            "query_type": "base"
        },
        "TITULAR_DREPT_ADMINISTRARE": {
            "individual": "PatrimoniuASE",
            "property": "titularaDreptAdministrareBunuriStat",
            "query_type": "base"
        },
        "PRINCIPII_COD_ETICA": {
            "individual": "PrincipiiCodEtica",
            "property": "integritate",
            "query_type": "base"
        },
        "COMPORTAMENT_FATA_STUDENTI": {
            "individual": "PrincipiiCodEtica",
            "property": "conduita",
            "query_type": "base"
        },
        "COOPERARE_COMUNITARA": {
            "individual": "PrincipiiCodEtica",
            "property": "cooperare",
            "query_type": "base"
        },
        "COMPONENTA_COMISIE_ETICA": {
            "individual": "PrincipiiEtice",
            "property": "compozitie",
            "query_type": "base"
        },
        "PRINCIPII_CONDUITA": {
            "individual": "PrincipiiEtice",
            "property": "principiiConduita",
            "query_type": "nodes",
            "node_properties": ["conduitaMoralaAdecvata", "evitareHartuire", "masuriAnticipativeSuprasolicitare", "solutionareNemultumiriCaleIerarhica"]
        },
        "CRITERII_EXCLUDERE": {
            "individual": "PrincipiiEtice",
            "property": "excludere",
            "query_type": "base"
        },
        "NUMIRE_PRODECAN": {
            "individual": "Prodecan",
            "property": "numitDe",
            "query_type": "base"
        },
        "DEMITERE_PRODECAN": {
            "individual": "Prodecan",
            "property": "poateFiiDemis",
            "query_type": "nodes",
            "node_properties": ["de"]
        },
        "SITUATII_DEMITERE_PRODECAN": {
            "individual": "Prodecan",
            "property": "poateFiiDemis",
            "query_type": "nodes",
            "node_properties": ["de", "situatii"]
        },
        "SARCINI_STABILITE_PRODECAN": {
            "individual": "Prodecan",
            "property": "sarciniStabiliteDe",
            "query_type": "base"
        },
        "ADMITERE_PROGRAME_STUDII": {
            "individual": "ProgrameDeStudii",
            "property": "admitere",
            "query_type": "nodes",
            "node_properties": ["condițiiCetățeni", "conformitateLegislație", "metodologiiProprii"]
        },
        "CALIFICARI_DOCUMENTE": {
            "individual": "ProgrameDeStudii",
            "property": "calificări",
            "query_type": "nodes",
            "node_properties": ["atestare", "documenteOficiale", "echivalență", "organizareComună"]
        },
        "ALOCARE_CREDITE": {
            "individual": "ProgrameDeStudii",
            "property": "crediteTransferabile",
            "query_type": "nodes",
            "node_properties": ["alocareConform", "elementReferință", "numărSpecific", "precizarePlanÎnvățământ",
                                "regulamente", "volumMuncăIntelectuală", "școliVarăȘiVoluntariat"]
        },
        "FORME_ORGANIZARE_STUDII": {
            "individual": "ProgrameDeStudii",
            "property": "formeleOrganizare",
            "query_type": "nodes",
            "node_properties": ["cuFrecvență", "cuFrecvențăRedusă", "laDistanță"]
        },
        "STRUCTURA_AN_UNIVERSITAR": {
            "individual": "ProgrameDeStudii",
            "property": "structurăAnUniversitar",
            "query_type": "nodes",
            "node_properties": ["aprobare", "conformitate"]
        },
        "TIPURI_PROGRAME_STUDII": {
            "individual": "ProgrameDeStudii",
            "property": "tipuriProgram",
            "query_type": "nodes",
            "node_properties": ["studiileFormareProfesionalăAdult", "studiileFormarePsihopedagogică",
                                "studiilePostuniversitare", "studiileUniversitare"]
        },
        "DURATA_MANDAT": {
            "individual": "Prorector",
            "property": "durataMandat",
            "query_type": "base"
        },
        "CONDITII_DEMITERE_PRORECTOR": {
            "individual": "Prorector",
            "property": "poateFiiDemis",
            "query_type": "nested_nodes",
            "node_properties": [
                {
                    "name": "de",
                    "type": "simple"
                },
                {
                    "name": "motiv",
                    "type": "nested",
                    "properties": [
                        {"name": "incalcareLegislatieNormeEtica"},
                        {"name": "incompatibilitateLegala"},
                        {"name": "nendeplinireSarcini"},
                        {"name": "prejudiciuIntereseASE"}
                    ]
                }
            ]
        },
        "SARCINI_PRORECTOR": {
            "individual": "Prorector",
            "property": "sarcini",
            "query_type": "nodes",
            "node_properties": [
                "activitatiSocialeCulturaleSportive",
                "alteAtributii",
                "asigurareCalitate",
                "atragereFonduriEuropene",
                "cercetareDezvoltareInovare",
                "conservareaPatrimoniuluiASE",
                "finantareaInvestitiiActivitatiBaza",
                "managementFinanciar",
                "managementLogisticaInfrastructura",
                "managementResurseUmane",
                "organizareFonduriEuropene",
                "organizareProgramStudii",
                "parteneriatePlanNational",
                "relatiiInternationale",
                "relatiiPublicePromovareASE",
                "viataStudenteasca"
            ]
        },
        "ASIGURARE_CALITATE": {
            "individual": "Prorector",
            "property": "sarcini",
            "query_type": "nodes",
            "node_properties": [
                "asigurareCalitate",
            ]
        },
        "ATRAGERE_FONDURI_EUROPENE": {
            "individual": "Prorector",
            "property": "sarcini",
            "query_type": "nodes",
            "node_properties": [
                "atragereFonduriEuropene"
            ]
        },
        "ORGANIZARE_PROGRAM_STUDII": {
            "individual": "Prorector",
            "property": "sarcini",
            "query_type": "nodes",
            "node_properties": [
                "organizareProgramStudii"
            ]
        },
        "RELAȚII_INTERNAȚIONALE": {
            "individual": "Prorector",
            "property": "sarcini",
            "query_type": "nodes",
            "node_properties": [
                "relatiiInternationale"
            ]
        },
        "ATRIBUTII_RECTOR": {
            "individual": "Rector",
            "property": "atributii",
            "query_type": "nested_nodes",
            "node_properties": [
                {"name": "alocareFonduriStimulare", "type": "simple"},
                {"name": "anulareCertificatDiplomaFrauduloasa", "type": "simple"},
                {"name": "aplicarePrevederiRegulamentIntern", "type": "simple"},
                {"name": "aplicareRaspunderePublica", "type": "nested", "properties": [
                    {"name": "declarareCapacitateScolarizare"},
                    {"name": "prezentareRaportStareaASE"},
                    {"name": "publicareDecizii"}
                ]},
                {"name": "aprobareAtributiiPersonalDidacticAuxiliar", "type": "simple"},
                {"name": "aprobareComponențaStructuraComisieiEtica", "type": "simple"},
                {"name": "asigurareBunaDesfasurareConcursuri", "type": "simple"},
                {"name": "atributiiAltele", "type": "simple"},
                {"name": "conducereConsiliulAdministratie", "type": "simple"},
                {"name": "conducereOperativaASE", "type": "simple"},
                {"name": "convocareSenatExtraordinar", "type": "simple"},
                {"name": "deciziiAngajareSancționare", "type": "simple"},
                {"name": "deciziiRegimMatricol", "type": "simple"},
                {"name": "gestionarePatrimoniuASE", "type": "simple"},
                {"name": "organizareConcursDecani", "type": "simple"},
                {"name": "organizareConcursPosturiDidacticeCercetare", "type": "simple"},
                {"name": "prezentareRapoarteSenat", "type": "simple"},
                {"name": "prezidareComisieConcursDirectorGeneral", "type": "simple"},
                {"name": "propunereReorganizareDesfiintare", "type": "simple"},
                {"name": "propunereRepetareExamenMedical", "type": "simple"},
                {"name": "propunereStructuraReglementariASE", "type": "simple"},
                {"name": "semnareActeOficiale", "type": "simple"},
                {"name": "supunereProiectBuget", "type": "simple"}
            ]
        },
        "DESEMNARE_RECTOR": {
            "individual": "Rector",
            "property": "desemnare",
            "query_type": "base"
        },
        "DURATA_MANDAT_RECTOR": {
            "individual": "Rector",
            "query_type": "all_properties",
            "filterCondition": "FILTER(STRSTARTS(STR(?property), STR(ase:)))"
        },
        "CONDITII_DEMITERE_RECTOR": {
                "individual": "Rector",
                "property": "poateFiiDemis",
                "query_type": "nested_nodes",
                "node_properties": [
                    {
                        "name": "de",
                        "type": "simple"
                    },
                    {
                        "name": "situatii",
                        "type": "nested",
                        "properties": [
                            {"name": "incalcareLegislatieNormeEtica", "type": "simple"},
                            {"name": "incompatibilitateLegala", "type": "simple"},
                            {"name": "neindeplinireIndicatori", "type": "simple"},
                            {"name": "prejudiciuInteresePrestigiuASE", "type": "simple"}
                        ]
                    }
                ]
        },
        "CONTRIBUIE_CONDUCERE_OPERATIONALA": {
            "individual": "Rector",
            "property": "conducereOperativaASE",
            "query_type": "base"
        },
        "ASIGURARE_BUNA_DESFASURARE_CONCURSURI": {
            "individual": "Rector",
            "property": "asigurareBunaDesfasurareConcursuri",
            "query_type": "base"
        },
        "ROL_GESTIONARE_PATRIMONIU": {
            "individual": "Rector",
            "property": "gestionarePatrimoniuASE",
            "query_type": "base"
        },
        "ROL_MEMBRU_FONDATOR_USASE": {
            "individual": "RelatieUSASE",
            "property": "membruFondator",
            "query_type": "base"
        },
        "PARTICIPARE_ORGANIZARE_ALEGERI": {
            "individual": "RelatieUSASE",
            "property": "partenerOrganizare",
            "query_type": "base"
        },
        "REPREZENTARE_INTERESE_STUDENTI": {
            "individual": "RelatieUSASE",
            "property": "reprezentareInterese",
            "query_type": "base"
        },
        "SUSTINERE_ACTIVITATE_USASE": {
            "individual": "RelatieUSASE",
            "property": "sustinereActivitate",
            "query_type": "base"
        },
        "CONTRACTE_OPERATIUNI_FINANCIARE": {
            "individual": "RelatiiParteneriatASE",
            "property": "contracteOperatiuniFinanciare",
            "query_type": "base"
        },
        "COOPERARE_INTERNATIONALA_PROCEDURA": {
            "individual": "RelatiiParteneriatASE",
            "property": "cooperareInternationalaProcedura",
            "query_type": "base"
        },
        "PARTICIPARE_ASOCIATII_CONSORTII": {
            "individual": "RelatiiParteneriatASE",
            "property": "participareAsociatiiConsorții",
            "query_type": "base"
        },
        "PROMOVARE_VALORI_EDUCATIE_CERCETARE": {
            "individual": "RelatiiParteneriatASE",
            "property": "promovareValoriSpațiuEuropeanInvatamantSuperiorCercetareStiintifica",
            "query_type": "base"
        },
        "ALEGERE_REPREZENTANTI_STUDENTI": {
            "individual": "ReprezentareStudentilor",
            "property": "aleagaReprezentantii",
            "query_type": "base"
        },
        "DESEMNARE_MEMBRI_REPREZENTANTI": {
            "individual": "ReprezentareStudentilor",
            "property": "desemnareMembri",
            "query_type": "base"
        },
        "PARTICIPARE_PROCES_DECIZIONAL": {
            "individual": "ReprezentareStudentilor",
            "property": "participareProcesDecizional",
            "query_type": "base"
        },
        "ROL_STUDENTI_DESEMNARE_RECTOR": {
            "individual": "ReprezentareStudentilor",
            "property": "participareProcesDesemnare",
            "query_type": "base"
        },
        "REPREZENTANT_CONSILIU_ADMINISTRATIE": {
            "individual": "ReprezentareStudentilor",
            "property": "reprezentantConsiliuAdministratie",
            "query_type": "base"
        },
        "GESTIUNE_PROTEJARE_RESURSE": {
            "individual": "ResurseASE",
            "property": "gestiuneProtejareResurse",
            "query_type": "base"
        },
        "MASURI_ADMINISTRARE_RESURSE": {
            "individual": "ResurseASE",
            "property": "masuriAdministrareResurseMaterialeFinanciare",
            "query_type": "base"
        },
        "RECUPERARE_PREJUDICII_PATRIMONIU": {
            "individual": "ResurseASE",
            "property": "recuperarePrejudiciiPatrimoniu",
            "query_type": "base"
        },
        "APLICABIL_PERSONAL_DIDACTIC": {
            "individual": "SancțiuniPersonalDidactic",
            "property": "aplicabil",
            "query_type": "base"
        },
        "TIPURI_SANCTIUNI_PERSONAL_DIDACTIC": {
            "individual": "SancțiuniPersonalDidactic",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "APLICABIL_STUDENTI": {
            "individual": "SancțiuniStudenti",
            "property": "aplicabil",
            "query_type": "base"
        },
        "TIPURI_SANCTIUNI_STUDENTI": {
            "individual": "SancțiuniStudenti",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "DIZOLVARE_SENAT": {
            "individual": "SenatInExercitiu",
            "property": "dizolvare",
            "query_type": "base"
        },
        "ORGANIZARE_REFERENDUM": {
            "individual": "SenatInExercitiu",
            "property": "organizareReferendum",
            "query_type": "base"
        },
        "ELABORARE_METODOLOGIE_ALEGERI": {
            "individual": "SenatInExercitiu",
            "property": "elaborareMetodologieAlegeri",
            "query_type": "base"
        },
        "APLICABIL_PERSONAL_DIDACTIC": {
            "individual": "SancțiuniPersonalDidactic",
            "property": "aplicabil",
            "query_type": "base"
        },
        "TIPURI_SANCTIUNI_PERSONAL_DIDACTIC": {
            "individual": "SancțiuniPersonalDidactic",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "APLICABIL_STUDENTI": {
            "individual": "SancțiuniStudenti",
            "property": "aplicabil",
            "query_type": "base"
        },
        "TIPURI_SANCTIUNI_STUDENTI": {
            "individual": "SancțiuniStudenti",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "DIZOLVARE_SENAT": {
            "individual": "SenatInExercitiu",
            "property": "dizolvare",
            "query_type": "base"
        },
        "ORGANIZARE_REFERENDUM": {
            "individual": "SenatInExercitiu",
            "property": "organizareReferendum",
            "query_type": "base"
        },
        "ELABORARE_METODOLOGIE_ALEGERI": {
            "individual": "SenatInExercitiu",
            "property": "elaborareMetodologieAlegeri",
            "query_type": "base"
        },
        "ADOPTARE_REGULAMENT": {
            "individual": "SenatulUniversitar",
            "property": "adoptareRegulament",
            "query_type": "base"
        },
        "ATRIBUTII_APROBARE_ACTIVITATI": {
            "individual": "SenatulUniversitar",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type && CONTAINS(STR(?property), 'atributieAprobare'))"
        },
        "STRUCTURA_SENATULUI": {
            "individual": "SenatulUniversitar",
            "property": "compozitie",
            "query_type": "base"
        },
        "CONDITII_REPREZENTARE_STUDENTI": {
            "individual": "SenatulUniversitar",
            "property": "conditiiReprezentareStudenți",
            "query_type": "base"
        },
        "CONDUCERE_SENAT": {
            "individual": "SenatulUniversitar",
            "property": "conducere",
            "query_type": "base"
        },
        "GARANTII_SENAT": {
            "individual": "SenatulUniversitar",
            "property": "garanteazaLibertatea",
            "query_type": "base"
        },
        "DURATA_MANDAT_SENAT": {
            "individual": "SenatulUniversitar",
            "property": "mandat",
            "query_type": "base"
        },
        "ORGANIZARE_SEDINTE": {
            "individual": "SenatulUniversitar",
            "property": "sedinte",
            "query_type": "base"
        },
        "CALITATEA_DE_STUDENT": {
            "individual": "StatutulStudentilor",
            "property": "calitateaDeStudent",
            "query_type": "base"
        },
        "CONDITII_FINANTARE": {
            "individual": "StatutulStudentilor",
            "property": "finantareDeLaBuget",
            "query_type": "base"
        },
        "SUBVENTIE_FINANCIARA": {
            "individual": "StatutulStudentilor",
            "property": "subventieFinanciaraBursa",
            "query_type": "base"
        },
        "COORDONARE_ACTIVITATE": {
            "individual": "StructuraServiciiTehnicoAdministrative",
            "property": "coordonație",
            "query_type": "base"
        },
        "STRUCTURI_EDUCATIE_CERCETARE": {
            "individual": "StructuraServiciiTehnicoAdministrative",
            "property": "structuraEducatieCercetare",
            "query_type": "nodes",
            "node_properties": ["alteStructuri", "centruÎnvățământLaDistanțăȘiFrecvențăRedusă", "departamente", "facultăți", "incubatoareDeAfaceri", "instituteȘiCentreDeCercetare", "unitățiPrestăriDeServicii", "școliDoctoraleȘiPostdoctorale", "școliPostuniversitare"]
        },
        "STRUCTURA_SERVICII_TEHNICO_ADMINISTRATIVE": {
            "individual": "StructuraServiciiTehnicoAdministrative",
            "property": "structuraServiciiTehnicoAdministrative",
            "query_type": "nodes",
            "node_properties": [
                "bazeSportive",
                "bibliotecă",
                "editură",
                "muzee",
                "serviciiTehnicoAdministrative",
                "tipografie",
                "unitățiDeAgrementȘiSociale"
            ]
        },
        "STRUCTURI_CONDUCERE": {
            "individual": "StructurileUniversitareConducere",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "VALORI_FUNDAMENTALE": {
            "individual": "Valori",
            "query_type": "all_properties",
            "filter_condition": "FILTER (?property != rdf:type)"
        },
        "DEFINITIE_INTEGRITATE": {
            "individual": "Valori",
            "property": "integritate",
            "query_type": "base"
        },
        "PROFESIONALISM": {
            "individual": "Valori",
            "property": "profesionalism",
            "query_type": "base"
        },
        "ASIGURAREA_CALITATII": {
            "individual": "Viziune",
            "property": "asigurareaCalitatii",
            "query_type": "base"
        },
        "AUTONOMIA_UNIVERSITARA": {
            "individual": "Viziune",
            "property": "autonomiaUniversitara",
            "query_type": "base"
        },
        "CENTRAREA_EDUCATIEI_PE_STUDENT": {
            "individual": "Viziune",
            "property": "centrareaEducatieiPeStudent",
            "query_type": "base"
        },
        "EFICACITATEA_MANAGERIALA_SI_EFICIENTA_FINANCIARA": {
            "individual": "Viziune",
            "property": "eficacitateaManagerialăȘiEficiențaFinanciară",
            "query_type": "base"
        },
        "INDEPENDENTA_FATA_DE_IDEOLOGII": {
            "individual": "Viziune",
            "property": "independențaFațăDeIdeologii",
            "query_type": "base"
        },
        "LIBERTATEA_ACADEMICA": {
            "individual": "Viziune",
            "property": "libertateaAcademica",
            "query_type": "base"
        },
        "LIBERTATEA_DE_MOBILITATE": {
            "individual": "Viziune",
            "property": "libertateaDeMobilitate",
            "query_type": "base"
        },
        "PARTENERIATUL_CU_ENTITATI": {
            "individual": "Viziune",
            "property": "parteneriatulCuEntități",
            "query_type": "base"
        },
        "TRANSPARENTA_DECIZIONALA": {
            "individual": "Viziune",
            "property": "transparențaDecizională",
            "query_type": "base"
        },
        "INTREBARI": {
            "query_type": "special"
        },

}

def form_sparql_query(entities):
    base_query = '''
               PREFIX ase: <http://www.ase.ro#>
               SELECT ?value
               WHERE {{
                   ase:{individual} ase:{property} ?value.
               }}
           '''

    base_query_nodes = '''
               PREFIX ase: <http://www.ase.ro#>
               SELECT ?{nodeProperties}
               WHERE {{
                   ase:{individual} ase:{property} ?node.
                   {nodeConditions}
               }}
           '''

    base_query_all_properties = '''
                  PREFIX ase: <http://www.ase.ro#>
                  PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                  SELECT ?property ?value
                  WHERE {{
                      ase:{individual} ?property ?value.
                      {filterCondition}
                  }}
              '''

    base_query_nested_nodes = '''
            PREFIX ase: <http://www.ase.ro#>
            SELECT {variables}
            WHERE {{
                ase:{individual} ase:{property} ?node.
                {conditions}
            }}
        '''

    for entity_text, entity_label in entities:
        if entity_label in entity_mapping:
            mapping = entity_mapping[entity_label]
            query_type = mapping.get("query_type")

            if query_type == "special":
                return None, entity_label

            query_individual = mapping["individual"]
            query_property = mapping.get("property")


            if query_type == "base":
                sparql_query_string = base_query.format(individual=query_individual, property=query_property)
            elif query_type == "nodes":
                node_properties = mapping.get("node_properties", [])
                node_conditions = [f"?node ase:{prop} ?{prop}." for prop in node_properties]
                sparql_query_string = base_query_nodes.format(
                    individual=query_individual,
                    property=query_property,
                    nodeProperties=' ?'.join(node_properties),
                    nodeConditions=' '.join(node_conditions)
                )
            elif query_type == "all_properties":
                filter_condition = mapping.get("filter_condition", "")
                sparql_query_string = base_query_all_properties.format(
                    individual=query_individual,
                    filterCondition=filter_condition
                )
            elif query_type == "nested_nodes":
                conditions = []
                variables = []
                for prop in mapping["node_properties"]:
                    if prop["type"] == "simple":
                        conditions.append(f"?node ase:{prop['name']} ?{prop['name']}.")
                        variables.append(f"?{prop['name']}")
                    elif prop["type"] == "nested":
                        sub_node_var = f"?{prop['name']}Node"
                        conditions.append(f"?node ase:{prop['name']} {sub_node_var}.")
                        for sub_prop in prop["properties"]:
                            conditions.append(f"{sub_node_var} ase:{sub_prop['name']} ?{sub_prop['name']}.")
                            variables.append(f"?{sub_prop['name']}")

                sparql_query_string = base_query_nested_nodes.format(
                    individual=query_individual,
                    property=query_property,
                    variables=' '.join(variables),
                    conditions=' '.join(conditions)
                )
            return sparql_query_string, entity_label

    return None, None

def execute_sparql_query(query):
    sparql_endpoint = "http://localhost:3030/CartaASE/query"
    sparql = SPARQLWrapper(sparql_endpoint)
    sparql.setReturnFormat(JSON)
    sparql.setQuery(query.encode('utf-8'))
    results = sparql.query().convert()
    return results
