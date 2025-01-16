# Mapping da https://www.cun.it/uploads/storico/settori_scientifico_disciplinari_english.pdf
# (consiglio universitario nazionale)
COURSE_MAPPINGS_IT = {
    # 1
    "scienze statistiche": "matematica",
    
    # --> 'psicologia'
    # 11E
    'psychology': 'psicologia',
    'psychologia': 'psicologia',
    'scienze psicologiche': 'psicologia',
    'psicologia clinica': 'psicologia',
    "scienze cognitive": "psicologia",  # According to the same data from MUR used for MAP_SSD_TO_STEM

    # --> 'scienze politiche e relazioni internazionali'
    # 14/A
    # (14/B is "storia politica", including "storia delle relazioni internazionali"
    'scienze politiche e delle relazioni internazionali': 'scienze politiche e relazioni internazionali',
    'scienze politiche': 'scienze politiche e relazioni internazionali',
    'relazioni internazionali': 'scienze politiche e relazioni internazionali',
    'scienze internazionali e diplomatiche': 'scienze politiche e relazioni internazionali',

    "sociologia": "scienze sociali",

    # 10 (10/G and others)
    'lingue e culture moderne': 'lettere',
    'lingue e letterature moderne': 'lettere',
    'lingua e letterature moderne': 'lettere',
    'lingua e letterature straniere moderne': 'lettere',
    'lettere moderne': 'lettere',
    'letteratura moderna e contemporanea': 'lettere',
    'letterature moderne': 'lettere',
    #
    'letteratura': 'lettere',
    'letteratura italiana': 'lettere',
    'letteratura comparata': 'lettere',
    'letterature comparate': 'lettere',
    'lingua e letteratura italiana': 'lettere',
    # --> 'letterature straniere'
    'lingue e letterature straniere': 'lettere',
    'lingua e letterature straniere': 'lettere',
    'letterature e lingue straniere': 'lettere',
    'letteratura, lingue e culture straniere': 'lettere',
    'lingue e letterature straniere moderne': 'lettere',
    'lingue e culture straniere': 'lettere',
    'lingua e letteratura inglese': 'lettere',
    # --> linguistica
    'linguistica': 'lettere',
    'linguistica applicata': 'lettere',
    'linguistica e letteratura italiana': 'lettere',
    'linguistica e letterature comparate': 'lettere',
    'linguistica italiana': 'lettere',
    #
    "mediazione linguistica e culturale": "lingue",
    "mediazione linguistica": "lingue",
    "lingue e mediazione linguistica": "lingue",

    # Filosofia is actually *11/C*
    # --> 'lettere e filosofia'
    'lettere e filosofia': 'filosofia',
    'letteratura e filosofia': 'filosofia',
    'letterature e filosofia': 'filosofia',

    # --> beni culturali
    # 10
    'conservazione dei beni culturali': 'beni culturali',

    # 10/A
    # --> archeologia
    'scienze archeologiche': 'archeologia',

    # 11/A
    # --> storia
    'scienze storiche': 'storia',

    # 05 – SCIENZE BIOLOGICHE
    # --> 'biologia'
    'biologia o scienze biologiche': 'biologia',
    'scienze biologiche': 'biologia',

    # 13 – SCIENZE ECONOMICHE E STATISTICHE    
    # --> 'economia e management'
    # 13/B – Economia aziendale
    'economia e finanza': 'economia e management',
    'economia e gestione aziendale': 'economia e management',
    'economia aziendale': 'economia e management',
    'economia e commercio': 'economia e management',
    'economia e commercio internazionale': 'economia e management',
    'economia': 'economia e management',
    'scienze economiche': 'economia e management',
    'scienze economiche e bancarie': 'economia e management',
    'scienze economiche e aziendali': 'economia e management',
    'scienze economiche e finanziarie': 'economia e management',
    'scienze economiche e gestionali': 'economia e management',
    'economia e gestione delle imprese': 'economia e management',
    'management e consulenza aziendale': 'economia e management',
    "management e comunicazione d'impresa": 'economia e management',
    'management internazionale': 'economia e management',

    # 08 – INGEGNERIA CIVILE E ARCHITETTURA
    # 08/C – Design e progettazione tecnologica dell'architettura
    # --> 'design'
    'design e arti visive': 'design',
    'design e arti': 'design',
    'arti e design': 'design',
    'arte e design': 'design',
    'design della comunicazione': 'design',  # design della comunicazione as different category?? ## TODO: could also be "comunicazione e marketing"
    'design e comunicazione': 'design',
    'design e comunicazione visiva': 'design',
    "design del prodotto e dell'innovazione": 'design',  # or 'design del prodotto' as different category??
    "design del prodotto e dell'evento": 'design',
    "design del prodotto": 'design',
    "design del prodotto industriale": 'design',
    "design industriale": 'design',

    "scienze biomediche": "ingegneria biomedica",  # is this ok?

    #
    # 06 – SCIENZE MEDICHE
    'medicina': 'medicina e chirurgia',

    # Non ce n'e' uno chiaro!
    # 14 – SCIENZE POLITICHE E SOCIALI	
    'comunicazione e media digitali': 'comunicazione e media',
    'comunicazione digitale': 'comunicazione e media',
    'comunicazione': 'comunicazione e media',
    'comunicazione e giornalismo': 'comunicazione e media',
    'comunicazione e tecniche giornalistiche': 'comunicazione e media',
    'comunicazione e relazioni pubbliche': 'comunicazione e media',
    'scienze della comunicazione': 'comunicazione e media',
    'comunicazione e marketing digitale': 'comunicazione e media',

    # 01 – Scienze matematiche e informatiche
    'scienze e tecnologie informatiche': 'informatica',
    'scienze informatiche': 'informatica',
    'data science e intelligenza artificiale': 'data science e artificial intelligence',
    'data science': 'data science e artificial intelligence',
    'scienze dei dati': 'data science e artificial intelligence',

    # 11 – Scienze storiche, filosofiche, pedagogiche e psicologiche
    "scienze della formazione primaria": "scienze dell'educazione",
    "scienze della formazione": "scienze dell'educazione",

    # 8
    "scienze dell'architettura": "architettura",
}

MAPPING_TO_SSD = {
    "NONE": "NONE",
    "scienze": "NONE", # unacceptable response
    "matematica": "01",
    "informatica": "01",
    "data science e artificial intelligence": "01",
    "scienze geologiche": "04",
    "scienze naturali": "04",
    "biologia": "05",
    "biotecnologie": "05",
    "medicina e chirurgia": "06",
    "scienze infermieristiche": "06",
    "scienze ambientali": "07",  #  - Scienze agrarie e veterinarie",    # Scienze e tecnologie forestali ed ambientali		Forestry	No
    "medicina veterinaria": "07",  #  - Scienze agrarie e veterinarie",    # Scienze e tecnologie forestali ed ambientali		Forestry	No
    "design": "08",
    "architettura": "08",
    "ingegneria civile": "08",
    "ingegneria": "09",  # seems quite rare
    "tecnologie": "09",  # very rare, but should we ignore it?
    "ingegneria informatica": "09",
    "ingegneria meccanica": "09",
    "ingegneria biomedica": "09",
    "ingegneria gestionale": "09",  # this one I really don't like, but it is like this in the MUR data
    "beni culturali": "10",
    "archeologia": "10",
    "lettere": "10",
    "lingue": "10",
    "scienze umanistiche": "11",  # Could also be others, eg 10
    "scienze umane": "11",  # Could also be others, eg 10
    "filosofia": "11",
    "psicologia": "11",
    "storia": "11",
    "scienze dell'educazione": "11",
    "scienze motorie": "11",  # "metodi e didattiche attività sportive"
    "giurisprudenza":  "12",  # - Scienze giuridiche
    "economia e management": "13",
    "comunicazione e media": "14",
    "scienze politiche e relazioni internazionali": "14",
    "scienze sociali": "14",
}

# This second mapping is done by using data from the following link:
# https://dati-ustat.mur.gov.it/dataset/dati-per-bilancio-di-genere/resource/3f52db2f-24ce-4605-8e51-5618cc4ff4e3
MAP_SSD_TO_STEM = {
    "NONE": "NONE",
    "01": True,
    "04": True,
    "05": True,
    "06": False,  # Do we want the STEM or STEMM grouping? (with or without Medicina)
    "07": False,
    "08": True,
    "09": True,
    "10": False,
    "11": False,
    "12": False,
    "13": False,
    "14": False,
}
