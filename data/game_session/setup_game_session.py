from sqlalchemy import create_engine, Column, String, Integer, JSON, Enum, CheckConstraint
from sqlalchemy.orm import declarative_base, sessionmaker

# Creazione del database SQLite con SQLAlchemy
DATABASE_URL = "sqlite:///game_session.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

# 1️⃣ Definizione della tabella `party`
class Party(Base):
    __tablename__ = "party"

    id = Column(String, primary_key=True)  # ID personalizzato "pg_{i}"
    stats = Column(JSON, nullable=False)  # Dizionario JSON per le statistiche
    indossa = Column(JSON, nullable=False)  # Dizionario JSON per l'inventario
    meta_stats = Column(JSON, nullable=False)  # Dizionario JSON per meta-dati

# 2️⃣ Definizione della tabella `inventario`
class Inventario(Base):
    __tablename__ = "inventario"

    id = Column(Integer, primary_key=True, autoincrement=True)  # ID autoincrementale
    categoria = Column(Enum("CHIAVE", "EQUIP", "CONSUMABILE", name="categoria_enum"), nullable=False)  # Enum categoria
    quantita = Column(Integer, nullable=False)  # Quantità tra 1 e 99

    __table_args__ = (
        CheckConstraint("quantita BETWEEN 1 AND 99", name="check_quantita_range"),  # Vincolo quantità
    )

# Creazione delle tabelle nel database
Base.metadata.create_all(engine)

# Creazione della sessione
Session = sessionmaker(bind=engine)
session = Session()

# 3️⃣ Popolamento della tabella `party` con dati di esempio
hero = Party(id=f"pg_0",
          stats={"forza": 20, "destrezza": 6, "magia": 15},  # Placeholder
          indossa={"pozione": 2, "spada": 1},  # Placeholder
          meta_stats={"exp": 100, "livello": 2,"razza":"bangaa__razza","classe":"mago_nero__classe"})
# 2️⃣ Popolamento della tabella con dati di esempio
party_members = [
    Party(id=f"pg_{i+1}",
          stats={"forza": 10+i, "destrezza": 10-i, "magia": 10-i},  # Placeholder
          indossa={"pozione": 2+i, "spada": 1},  # Placeholder
          meta_stats={"exp": 100+2*i, "livello": 2,"razza":"bangaa__razza","classe":"Gladiator"})  # Placeholder
    for i in range(3)  # Crea 5 membri del party (pg_0, pg_1, ...)
]
party_members=[hero,*party_members]

# 4️⃣ Popolamento della tabella `inventario` con dati di esempio
inventario_items = [
    Inventario(categoria="CHIAVE", quantita=1),
    Inventario(categoria="EQUIP", quantita=3),
    Inventario(categoria="CONSUMABILE", quantita=10),
    Inventario(categoria="EQUIP", quantita=5),
    Inventario(categoria="CONSUMABILE", quantita=99)  # Quantità massima
]

# Inserimento dati nel database
session.add_all(party_members)
session.add_all(inventario_items)
session.commit()
session.close()

print("✅ Tabelle `party` e `inventario` create e popolate con dati di esempio!")
