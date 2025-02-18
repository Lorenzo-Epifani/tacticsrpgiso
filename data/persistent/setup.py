import sqlite3
import uuid

PERSISTENT_DB = "persistent.db"

def generate_uuid():
    """Genera un UUID stringa per usarlo come PRIMARY KEY"""
    return str(uuid.uuid4())

def create_database():
    """Crea il database e tutte le tabelle"""
    conn = sqlite3.connect(PERSISTENT_DB)
    cursor = conn.cursor()

    # Abilita chiavi esterne
    cursor.execute("PRAGMA foreign_keys = ON;")

    # 1️⃣ Razza
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Razza (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE
        );
    """)

    # 2️⃣ Classe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Classe (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            requisiti TEXT
        );
    """)

    # Tabella ponte Razza <-> Classe (N:N)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Razza_Classe (
            razza_id TEXT NOT NULL,
            classe_id TEXT NOT NULL,
            PRIMARY KEY (razza_id, classe_id),
            FOREIGN KEY (razza_id) REFERENCES Razza(id) ON DELETE CASCADE,
            FOREIGN KEY (classe_id) REFERENCES Classe(id) ON DELETE CASCADE
        );
    """)

    # 3️⃣ Equipaggiamento
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equip_Cat (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL CHECK(tipo IN ('ARMA', 'ARMATURA', 'CONSUMABILE'))
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equip (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            stats TEXT NOT NULL,
            equip_cat_id TEXT NOT NULL,
            FOREIGN KEY (equip_cat_id) REFERENCES Equip_Cat(id) ON DELETE CASCADE
        );
    """)

    # Tabella ponte Classe <-> Equip_Cat (N:N)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Classe_Equip_Cat (
            classe_id TEXT NOT NULL,
            equip_cat_id TEXT NOT NULL,
            PRIMARY KEY (classe_id, equip_cat_id),
            FOREIGN KEY (classe_id) REFERENCES Classe(id) ON DELETE CASCADE,
            FOREIGN KEY (equip_cat_id) REFERENCES Equip_Cat(id) ON DELETE CASCADE
        );
    """)

    # 4️⃣ Abilità
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Abilita (
            id TEXT PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            p_ab INTEGER NOT NULL,
            effect TEXT NOT NULL CHECK(effect IN ('DANNO', 'CURA', 'BUFF', 'DEBUFF'))
        );
    """)

    # Tabella ponte Equip <-> Abilita (N:N)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equip_Abilita (
            equip_id TEXT NOT NULL,
            abilita_id TEXT NOT NULL,
            PRIMARY KEY (equip_id, abilita_id),
            FOREIGN KEY (equip_id) REFERENCES Equip(id) ON DELETE CASCADE,
            FOREIGN KEY (abilita_id) REFERENCES Abilita(id) ON DELETE CASCADE
        );
    """)

    # 5️⃣ Specializzazione Abilità
    cursor.execute("CREATE TABLE IF NOT EXISTS Attiva (id TEXT PRIMARY KEY, FOREIGN KEY (id) REFERENCES Abilita(id) ON DELETE CASCADE);")
    cursor.execute("CREATE TABLE IF NOT EXISTS Passiva (id TEXT PRIMARY KEY, FOREIGN KEY (id) REFERENCES Abilita(id) ON DELETE CASCADE);")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reazione (
            id TEXT PRIMARY KEY,
            trigger TEXT NOT NULL CHECK(trigger IN ('DANNO_SUBITO', 'ATTACCO', 'MAGIA', 'MOVIMENTO')),
            FOREIGN KEY (id) REFERENCES Abilita(id) ON DELETE CASCADE
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Innata (
            id TEXT PRIMARY KEY,
            trigger TEXT NOT NULL CHECK(trigger IN ('BORN', 'LEVEL_UP', 'EVOLVE')),
            razza_id TEXT NOT NULL,
            FOREIGN KEY (id) REFERENCES Abilita(id) ON DELETE CASCADE,
            FOREIGN KEY (razza_id) REFERENCES Razza(id) ON DELETE CASCADE
        );
    """)

    conn.commit()
    conn.close()
    print("✅ Database creato con successo!")

def populate_database():
    """Inserisce dati di prova nel database"""
    conn = sqlite3.connect(PERSISTENT_DB)
    cursor = conn.cursor()

    # Inserimento Razze
    razze = [(generate_uuid(), "Umano"), (generate_uuid(), "Elfo")]
    cursor.executemany("INSERT INTO Razza (id, nome) VALUES (?, ?);", razze)

    # Inserimento Classi
    classi = [(generate_uuid(), "Guerriero", "{}"), (generate_uuid(), "Mago", "{}")]
    cursor.executemany("INSERT INTO Classe (id, nome, requisiti) VALUES (?, ?, ?);", classi)

    # Collegamento Razza <-> Classe
    cursor.execute("INSERT INTO Razza_Classe (razza_id, classe_id) VALUES (?, ?);", (razze[0][0], classi[0][0]))

    # Inserimento Categorie Equipaggiamento
    equip_categorie = [(generate_uuid(), "Spada", "ARMA"), (generate_uuid(), "Armatura Pesante", "ARMATURA")]
    cursor.executemany("INSERT INTO Equip_Cat (id, nome, tipo) VALUES (?, ?, ?);", equip_categorie)

    # Collegamento Classe <-> Equip_Cat
    cursor.execute("INSERT INTO Classe_Equip_Cat (classe_id, equip_cat_id) VALUES (?, ?);", (classi[0][0], equip_categorie[0][0]))

    # Inserimento Equipaggiamento
    equipaggiamenti = [(generate_uuid(), "Excalibur", '{"attacco": 50}', equip_categorie[0][0])]
    cursor.executemany("INSERT INTO Equip (id, nome, stats, equip_cat_id) VALUES (?, ?, ?, ?);", equipaggiamenti)

    # Inserimento Abilità
    abilita = [(generate_uuid(), "Colpo Critico", 10, "DANNO"), (generate_uuid(), "Sangue Reale", 0, "BUFF")]
    cursor.executemany("INSERT INTO Abilita (id, nome, p_ab, effect) VALUES (?, ?, ?, ?);", abilita)

    # Collegamento Equip <-> Abilità
    cursor.execute("INSERT INTO Equip_Abilita (equip_id, abilita_id) VALUES (?, ?);", (equipaggiamenti[0][0], abilita[0][0]))

    # Inserimento Abilità Attiva
    cursor.execute("INSERT INTO Attiva (id) VALUES (?);", (abilita[0][0],))

    # Inserimento Abilità Innata
    cursor.execute("INSERT INTO Innata (id, trigger, razza_id) VALUES (?, ?, ?);", (abilita[1][0], "BORN", razze[0][0]))

    conn.commit()
    conn.close()
    print("✅ Dati di prova inseriti con successo!")

# Eseguire il setup
create_database()
populate_database()
