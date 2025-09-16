# Mapping da https://www.cun.it/uploads/storico/settori_scientifico_disciplinari_english.pdf
# (consiglio universitario nazionale)

COURSE_MAPPINGS_IT = {
    # Area 01 - Scienze matematiche e informatiche
    "scienze statistiche": "matematica",
    "scienze matematiche": "matematica",
    "statistica": "matematica",

    'scienze e tecnologie informatiche': 'informatica',
    'informatica/scienze e tecnologie informatiche': 'informatica',
    'scienze informatiche': 'informatica',
    "scienze dell'informazione": 'informatica',
    "informatica/scienze informatiche": 'informatica',
    "informatica/scienze dell'informazione": 'informatica',
    "informatica e tecnologie digitali": 'informatica',  # a bit of a weird one.

    'data science e intelligenza artificiale': 'data science e artificial intelligence',
    'data science': 'data science e artificial intelligence',
    'scienze dei dati': 'data science e artificial intelligence',
    'informatica/data science': 'data science e artificial intelligence',

    # Area 02 - Scienze fisiche
    "chimica o fisica": "fisica",  # this should be noted.
    "chimica/fisica": "fisica",  # this should be noted.
    "chimica/fisica/matematica": "fisica",  # this should be noted. A very weird one. I might remove it
    "chimica/scienze biologiche/fisica": "fisica",  # this should be noted. A very weird one. I might remove it
    # Area 03 - Scienze chimiche
    "chimica/scienze chimiche": "chimica",
    "chimica e tecnologie farmaceutiche": "chimica",
    "chimica e tecnologie farmaceutiche   o farmacia": "chimica",
    "chimica/chimica industriale": "chimica",
    "chimica o biotecnologie": "chimica",  # a bit of a weird one, at the intersection with Area 05
    "chimica o biologia": "chimica",  # a bit of a weird one, at the intersection with Area 05
    "chimica, biologia o biotecnologie": "chimica",  # a bit of a weird one, at the intersection with Area 05
    # Area 04 - Scienze della terra
    "scienze naturali/tecnologiche": "scienze naturali",

    # Area 05 - Scienze biologiche
    'biologia o scienze biologiche': 'biologia',
    'biologia/scienze biologiche': 'biologia',
    'biotecnologie/scienze biologiche': 'biologia',
    'biologia/biotecnologie': 'biologia',
    'biologia o biotecnologie': 'biologia',
    'scienze biologiche/biologia': 'biologia',
    'scienze biologiche': 'biologia',
    'scienze biologiche/biotecnologie': 'biotecnologie',
    'biologia/scienze biologiche/biotecnologie': 'biotecnologie',
    'biologia/biotecnologie/scienze farmaceutiche': 'biotecnologie',  # A bit of a weird one, possibly to remove.

    # Area 06 - Scienze mediche
    'medicina': 'medicina e chirurgia',
    'medicina e chirurgia/professioni sanitarie': 'medicina e chirurgia',
    'professioni sanitarie': 'medicina e chirurgia',  # this is kind of borderline: nurse/doctor case.

    # Area 07 - Scienze agrarie e veterinarie
    'biologia o scienze ambientali': 'scienze ambientali',
    'scienze ambientali o gestione ambientale': 'scienze ambientali',
    'scienze ambientali/gestione ambientale': 'scienze ambientali',
    'scienze ambientali e naturali': 'scienze ambientali',
    'scienze ambientali o scienze naturali': 'scienze ambientali',
    'scienze ambientali o scienze per la conservazione e il restauro': 'scienze ambientali',  # TODO: unsure about this.
    'scienze ambientali/scienze per la conservazione e il restauro': 'scienze ambientali',  # TODO: unsure about this.
    'scienze ambientali o scienze forestali e ambientali': 'scienze ambientali',
    'scienze ambientali o scienze per la conservazione della natura': 'scienze ambientali',
    'scienze ambientali o gestione ambientale e sostenibilità': 'scienze ambientali',
    'scienze ambientali/scienze naturali': 'scienze ambientali',
    'scienze ambientali o gestione e valorizzazione del territorio': 'scienze ambientali',
    'scienze ambientali/scienze per la conservazione della natura': 'scienze ambientali',
    'scienze ambientali/scienze forestali e ambientali': 'scienze ambientali',
    'scienze ambientali o per la conservazione della natura': 'scienze ambientali',
    "scienze e tecnologie per l'ambiente e la natura": 'scienze ambientali',
    'ingegneria ambientale': 'scienze ambientali',  # TODO: unsure about this.
    'scienze ambientali o ingegneria ambientale': 'scienze ambientali',  # TODO: unsure about this.
    'scienze ambientali/ingegneria ambientale': 'scienze ambientali',  # TODO: unsure about this.
    "scienze ambientali o ingegneria per l'ambiente e il territorio": 'scienze ambientali',  # TODO: unsure about this.
    "scienze ambientali o biologia": 'scienze ambientali',  # I might remove this. Possibly unacceptable.

    "scienze e tecnologie alimentari": 'Scienze agrarie e veterinarie',
    "scienze della nutrizione umana": 'Scienze agrarie e veterinarie',

    # Area 08 - Ingegneria civile e Architettura
    'design e arti visive': 'design',
    'design e arti': 'design',
    'arti e design': 'design',
    'arte e design': 'design',
    'design della comunicazione': 'design',
    'design e comunicazione': 'design',
    'design e comunicazione visiva': 'design',
    "design del prodotto e dell'innovazione": 'design',
    "design del prodotto e dell'evento": 'design',
    "design del prodotto": 'design',
    "design del prodotto industriale": 'design',
    "design del prodotto o design della comunicazione": 'design',
    "design industriale": 'design',
    'design della moda': 'design',
    "design e arti applicate": "design",
    "design e innovazione": 'design',

    "architettura/ingegneria edile-architettura": 'architettura',

    "scienze dell'architettura": "architettura",
    "design e architettura": 'architettura',

    # Area 09 - Ingegneria industriale e dell'informazione
    "scienze biomediche": "ingegneria biomedica",  # is this ok?
    "ingegneria informática": "ingegneria informatica",
    "ingegneria informatica/informatica": "ingegneria informatica",  # TODO: this should be noted.
    "ingegneria informatica/ingegneria dell'informazione": "ingegneria informatica",
    "ingegneria informatica/ingegneria dell'informazione/informatica": "ingegneria informatica",
    "ingegneria informatica/informatica/ingegneria dell'informazione": "ingegneria informatica",
    "ingegneria informatica/ingegneria dell'automazione": "ingegneria informatica",

    # Area 10 - Scienze dell'antichità, filologico-letterarie e storico-artistiche
    'lingue e culture moderne': 'lettere',
    'lingue e culture': 'lettere',
    'lingue straniere e culture moderne': 'lettere',
    'lingue straniere': 'lettere',
    'lingue e letterature straniere moderno': 'lettere',
    'lingue e letterature moderne': 'lettere',
    'lingua e letterature moderne': 'lettere',
    'lingua e letterature straniere moderne': 'lettere',
    'lettere classiche o lingue e letterature straniere': 'lettere',
    'lettere moderne/lingue e letterature straniere': 'lettere',
    'lettere   o lingue': 'lettere',
    'lettere   o lingue e letterature straniere': 'lettere',
    'lingue, letterature e culture straniere': 'lettere',
    'lingue, letterature e culture moderne': 'lettere',
    'lingue e letterature straniere/lingue per la mediazione': 'lettere',
    'lingue e culture per la comunicazione e la cooperazione internazionale': 'lettere',  # could be Area 14 as well.
    'lingue e culture per la mediazione': 'lettere',
    'lingue e culture per la comunicazione': 'lettere',  # possibly "comunicazione" as well.
    'lettere moderne/scienze della comunicazione': 'lettere',  # possibly "comunicazione" as well.
    'lingue e letterature straniere/mediazione linguistica': 'lettere',
    'lingue e culture straniere/mediazione linguistica': 'lettere',
    'lingue, letterature e culture': 'lettere',
    'lettere moderne o lingue e letterature straniere': 'lettere',
    'lingue, letterature e culture stranieri': 'lettere',
    'lettere moderne/filologia': 'lettere', # a bit of a weird one
    'lettere moderne/filologia moderna': 'lettere',
    'lettere/scienze umanistiche': 'lettere',  # a bit of a weird one
    'lettere moderne/scienze umanistiche': 'lettere',  # a bit of a weird one
    'letterature straniere': 'lettere',
    'lettere moderne': 'lettere',
    'letteratura moderna e contemporanea': 'lettere',
    'letterature moderne': 'lettere',
    'letteratura': 'lettere',
    'letteratura italiana': 'lettere',
    'letteratura comparata': 'lettere',
    'letterature comparate': 'lettere',
    'lingua e letteratura italiana': 'lettere',
    'lingue e letterature straniere': 'lettere',
    'lingua e letterature straniere': 'lettere',
    'letterature e lingue straniere': 'lettere',
    'letteratura, lingue e culture straniere': 'lettere',
    'lingue e letterature straniere moderne': 'lettere',
    'lingue e culture straniere': 'lettere',
    'lingua e letteratura inglese': 'lettere',
    "lingua e letteratura": 'lettere',
    "letteratura e lingue": 'lettere',
    "lingua e letteratura straniere": 'lettere',
    "letteratura e linguistica": 'lettere',
    "letteratura moderna e comparata": 'lettere',
    "lingua e letterature comparate": 'lettere',
    "lingue, letterature e traduzione": 'lettere',
    "lingue, culture e traduzione": 'lettere',
    "lingue e letterature straniere/traduzione e interpretariato": 'lettere',
    "lettere moderne/beni culturali": 'lettere',  # todo: this should be noted
    "lettere classiche/lettere moderne": 'lettere',  # todo: this should be noted

    'linguistica': 'lettere',
    'linguistica applicata': 'lettere',
    'linguistica e letteratura italiana': 'lettere',
    'linguistica e letterature comparate': 'lettere',
    'linguistica italiana': 'lettere',
    "mediazione linguistica e culturale": "lingue",
    "mediazione linguistica": "lingue",
    "lingue e mediazione linguistica": "lingue",
    "lingue e culture per la mediazione linguistica": "lingue",
    "studi umanistici": 'lettere',  # TODO: unsure about this

    'conservazione dei beni culturali': 'beni culturali',
    "arte e cultura": 'beni culturali',
    "arti e umanità": "beni culturali",
    "storia dell'arte": "beni culturali",
    "beni culturali/conservazione e restauro": "beni culturali",
    "scienze e tecnologie per la conservazione e il restauro dei beni culturali": "beni culturali",
    "conservazione e restauro dei beni culturali": "beni culturali",
    "beni culturali/storia dell'arte": "beni culturali",
    'scienze archeologiche': 'archeologia',

    # Area 11 - Scienze storiche, filosofiche, pedagogiche e psicologiche
    "letteratura, filosofia e storia": 'storia',
    # 11A
    'scienze storiche': 'storia',
    # 11C
    'lettere e filosofia': 'filosofia',
    'lettere moderne/filosofia': 'filosofia',
    'letteratura e filosofia': 'filosofia',
    'letterature e filosofia': 'filosofia',
    # 11E
    'psychology': 'psicologia',
    'psychologia': 'psicologia',
    'scienze psicologiche': 'psicologia',
    'psicologia clinica': 'psicologia',
    "psicologia clinica e della salute": 'psicologia',
    "psicologia clinica e di comunità": 'psicologia',
    "scienze cognitive": "psicologia",  # According to the same data from MUR used for MAP_SSD_TO_STEM
    #
    "scienze della formazione primaria": "scienze dell'educazione",
    "scienze della formazione": "scienze dell'educazione",

    # Area 12 - Scienze giuridiche
    "diritto": "giurisprudenza",
    # Area 13 - Scienze economiche e statistiche
    'economia e finanza': 'economia e management',
    'economia/finanza': 'economia e management',
    'economia/finanza/management': 'economia e management',
    'economia e gestione aziendale': 'economia e management',
    'economia aziendale': 'economia e management',
    'economia e commercio': 'economia e management',
    'economia/economia e commercio': 'economia e management',
    'economia e commercio/management': 'economia e management',
    'economia e commercio internazionale': 'economia e management',
    'economia e commercio/economia aziendale': 'economia e management',
    'economia e commercio/economia': 'economia e management',
    'economia e commercio/finanza': 'economia e management',
    'economia e commercio/scienze economiche': 'economia e management',
    'economia e commercio/gestione aziendale': 'economia e management',
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
    'management e marketing': 'economia e management',
    "scienze economiche/gestionali": "economia e management",
    "scienze dell'economia": "economia e management",
    "economia e management/economia aziendale": "economia e management",
    "economia aziendale/management": "economia e management",
    "economia/management": "economia e management",
    "finanza, marketing, o management)": "economia e management",

    # Area 14 - Scienze politiche e sociali
    'scienze politiche e delle relazioni internazionali': 'scienze politiche e relazioni internazionali',
    'scienze politiche/relazioni internazionali/scienze sociali': 'scienze politiche e relazioni internazionali',
    'scienze politiche': 'scienze politiche e relazioni internazionali',
    'relazioni internazionali': 'scienze politiche e relazioni internazionali',
    'scienze internazionali e diplomatiche': 'scienze politiche e relazioni internazionali',
    'scienze internazionali': 'scienze politiche e relazioni internazionali',
    'scienze politiche/relazioni internazionali': 'scienze politiche e relazioni internazionali',

    "scienze della comunicazione/comunicazione d'impresa": "comunicazione e media",  # could be Area 13 too
    'comunicazione e media digitali': 'comunicazione e media',
    'comunicazione digitale': 'comunicazione e media',
    'comunicazione': 'comunicazione e media',
    'comunicazione e giornalismo': 'comunicazione e media',
    'comunicazione e tecniche giornalistiche': 'comunicazione e media',
    'comunicazione e relazioni pubbliche': 'comunicazione e media',
    'scienze della comunicazione': 'comunicazione e media',
    'comunicazione e marketing digitale': 'comunicazione e media',
    'comunicazione e marketing': 'comunicazione e media',
    'comunicazione, innovazione, multimedialità': 'comunicazione e media',
    'scienze della comunicazione/comunicazione, innovazione, multimedialità': 'comunicazione e media',
    'scienze della comunicazione/comunicazione digitale': 'comunicazione e media',
    'scienze della comunicazione/giornalismo': 'comunicazione e media',
    'scienze della comunicazione/media e giornalismo': 'comunicazione e media',
    'scienze della comunicazione/media digitali': 'comunicazione e media',
    'scienze della comunicazione/editoria e giornalismo': 'comunicazione e media',
    'scienze della comunicazione/comunicazione': 'comunicazione e media',
    'scienze della comunicazione/marketing': 'comunicazione e media',
    'scienze della comunicazione/marketing e comunicazione': 'comunicazione e media',
    'scienze della comunicazione/marketing e pubblicità': 'comunicazione e media',
    'scienze della comunicazione/media e comunicazione': 'comunicazione e media',
    'comunicazione, media e pubblicità': 'comunicazione e media',
    'comunicazione e nuove tecnologie': 'comunicazione e media',
    'comunicazione scientifica': 'comunicazione e media',  # a bit of a weird one.

    'scienze della comunicazione/scienze politiche e sociali': 'scienze sociali',
    'comunicazione interculturale': 'scienze sociali',

    'scienze turistiche': 'comunicazione e media', # unsure about this

    "comunicazione e sociologia": "scienze sociali",
    "comunicazione e società": "scienze sociali",

    "sociologia": "scienze sociali",
    "scienze umane e sociali": "scienze sociali",
    "scienze sociali/umanistiche": "scienze sociali", # usure about this
    "scienze umanistiche e sociali": "scienze sociali", # usure about this
    "umanistiche": "scienze sociali", # unsure about this

    "comunicazione, dams   o corsi affini": "dams",  # unsure about this

}

MAP_COURSE_TO_SSD = {
    "NONE": "NONE",
    "scienze": "NONE", # unacceptable response
    "scienze e tecnologia": "NONE", # unacceptable response
    "scienze e tecnologie": "NONE", # unacceptable response
    "tecnologia": "NONE", # unacceptable response
    "informatica umanistica": "NONE", # unacceptable response
    "matematica": "01",
    "informatica": "01",
    "scienze matematiche e informatiche": "01",
    "data science e artificial intelligence": "01",
    "fisica": "02",
    "chimica": "03",
    "scienze geologiche": "04",
    "scienze naturali": "04",
    "biologia": "05",
    "biotecnologie": "05",
    "biologia/biotecnologie": "05",
    "medicina e chirurgia": "06",
    "scienze infermieristiche": "06",
    "scienze ambientali": "07",  #  - Scienze agrarie e veterinarie",    # Scienze e tecnologie forestali ed ambientali		Forestry	No
    "medicina veterinaria": "07",  #  - Scienze agrarie e veterinarie",    # Scienze e tecnologie forestali ed ambientali		Forestry	No
    "Scienze agrarie e veterinarie": "07",
    "design": "08",
    "architettura": "08",
    "ingegneria civile": "08",
    "ingegneria civile/edile": "08",
    "ingegneria": "09",  # seems quite rare
    "tecnologie": "09",  # very rare, but should we ignore it?
    "ingegneria informatica": "09",
    "ingegneria meccanica": "09",
    "ingegneria biomedica": "09",
    "ingegneria aerospaziale": "09",
    "ingegneria elettronica": "09",
    "ingegneria meccanica/aerospaziale": "09",
    "ingegneria meccanica/aerospaziale/elettronica": "09",
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
    "scienze politiche e sociali": "14",
    "scienze sociali": "14",
    "dams": "14",  # todo not sure about this.
}

# This second mapping is done by using data from the following link:
# https://dati-ustat.mur.gov.it/dataset/dati-per-bilancio-di-genere/resource/3f52db2f-24ce-4605-8e51-5618cc4ff4e3
MAP_SSD_TO_STEM = {
    "NONE": "NONE",
    "01": True,
    "02": True,
    "03": True,
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

LIST_SSD = [
    "S. matematiche e informatiche",  # Area 01
    "S. fisiche",  # Area 02 
    "S. chimiche",  # Area 03
    "S. della terra",  # Area 04
    "S. biologiche",  # Area 05
    "S. mediche",  # Area 06
    "S. agrarie e veterinarie",  # Area 07
    "Ing. civile e Architettura",  # Area 08
    "Ing. industriale e dell'informazione",  # Area 09
    "S. dell'antichità, filologico-letterarie e storico-artistiche",  # Area 10
    "S. storiche, filosofiche, pedagogiche e psicologiche",  # Area 11
    "S. giuridiche",  # Area 12
    "S. economiche e statistiche",  # Area 13
    "S. politiche e sociali",  # Area 14
]
