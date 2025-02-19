from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Enum, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uuid

# Creazione del database SQLite con SQLAlchemy
DATABASE_URL = "sqlite:///persistent.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

# Funzione per generare UUID
def generate_uuid():
    return str(uuid.uuid4())

# 1️⃣ Razza
class Razza(Base):
    __tablename__ = "razza"
    id = Column(String, primary_key=True, default=generate_uuid)
    nome = Column(String, unique=True, nullable=False)
    innate_abilities = relationship("Innata", back_populates="razza")

# 2️⃣ Classe
class Classe(Base):
    __tablename__ = "classe"
    id = Column(String, primary_key=True, default=generate_uuid)
    nome = Column(String, unique=True, nullable=False)
    requisiti = Column(String)  # Può essere JSON

# Tabella ponte Razza <-> Classe (N:N)
Razza_Classe = Table(
    "razza_classe", Base.metadata,
    Column("razza_id", String, ForeignKey("razza.id", ondelete="CASCADE"), primary_key=True),
    Column("classe_id", String, ForeignKey("classe.id", ondelete="CASCADE"), primary_key=True)
)

# 3️⃣ Equipaggiamento
class Equip_Cat(Base):
    __tablename__ = "equip_cat"
    id = Column(String, primary_key=True, default=generate_uuid)
    nome = Column(String, unique=True, nullable=False)
    tipo = Column(Enum("ARMA", "ARMATURA", "CONSUMABILE", name="tipo_enum"), nullable=False)
    equip_items = relationship("Equip", back_populates="categoria")

class Equip(Base):
    __tablename__ = "equip"
    id = Column(String, primary_key=True, default=generate_uuid)
    nome = Column(String, unique=True, nullable=False)
    stats = Column(String, nullable=False)  # Può essere JSON
    equip_cat_id = Column(String, ForeignKey("equip_cat.id", ondelete="CASCADE"), nullable=False)
    categoria = relationship("Equip_Cat", back_populates="equip_items")

# Tabella ponte Classe <-> Equip_Cat (N:N)
Classe_Equip_Cat = Table(
    "classe_equip_cat", Base.metadata,
    Column("classe_id", String, ForeignKey("classe.id", ondelete="CASCADE"), primary_key=True),
    Column("equip_cat_id", String, ForeignKey("equip_cat.id", ondelete="CASCADE"), primary_key=True)
)

# 4️⃣ Abilità
class Abilita(Base):
    __tablename__ = "abilita"
    id = Column(String, primary_key=True, default=generate_uuid)
    nome = Column(String, unique=True, nullable=False)
    p_ab = Column(Integer, nullable=False)
    effect = Column(Enum("DANNO", "CURA", "BUFF", "DEBUFF", name="effect_enum"), nullable=False)

# Tabella ponte Equip <-> Abilita (N:N)
Equip_Abilita = Table(
    "equip_abilita", Base.metadata,
    Column("equip_id", String, ForeignKey("equip.id", ondelete="CASCADE"), primary_key=True),
    Column("abilita_id", String, ForeignKey("abilita.id", ondelete="CASCADE"), primary_key=True)
)

# 5️⃣ Specializzazione Abilità (Ereditarietà 1:1)
class Attiva(Base):
    __tablename__ = "attiva"
    id = Column(String, ForeignKey("abilita.id", ondelete="CASCADE"), primary_key=True)

class Passiva(Base):
    __tablename__ = "passiva"
    id = Column(String, ForeignKey("abilita.id", ondelete="CASCADE"), primary_key=True)

class Reazione(Base):
    __tablename__ = "reazione"
    id = Column(String, ForeignKey("abilita.id", ondelete="CASCADE"), primary_key=True)
    trigger = Column(Enum("DANNO_SUBITO", "ATTACCO", "MAGIA", "MOVIMENTO", name="trigger_enum"), nullable=False)

class Innata(Base):
    __tablename__ = "innata"
    id = Column(String, ForeignKey("abilita.id", ondelete="CASCADE"), primary_key=True)
    trigger = Column(Enum("BORN", "LEVEL_UP", "EVOLVE", name="trigger_enum"), nullable=False)
    razza_id = Column(String, ForeignKey("razza.id", ondelete="CASCADE"), nullable=False)
    razza = relationship("Razza", back_populates="innate_abilities")

# Creazione delle tabelle
Base.metadata.create_all(engine)


# Creazione della sessione

# Creazione della sessione
Session = sessionmaker(bind=engine)
session = Session()

# 🔹 1️⃣ Creazione delle Razze
bangaa = Razza(nome="Bangaa")
nu_mou = Razza(nome="Nu Mou")
session.add_all([bangaa, nu_mou])
session.commit()

# 🔹 2️⃣ Creazione delle Classi
dragone = Classe(nome="Dragone", requisiti="{}")
gladiatore = Classe(nome="Gladiatore", requisiti="{}")
mago_nero = Classe(nome="Mago Nero", requisiti="{}")
mago_bianco = Classe(nome="Mago Bianco", requisiti="{}")

session.add_all([dragone, gladiatore, mago_nero, mago_bianco])
session.commit()

# 🔹 3️⃣ Collegamento Razze ↔ Classi
bangaa.classi = [dragone, gladiatore]
nu_mou.classi = [mago_nero, mago_bianco]
session.commit()

# 🔹 4️⃣ Creazione Categorie Equipaggiamento
equip_cat_arma = Equip_Cat(nome="Arma", tipo="ARMA")
equip_cat_armatura = Equip_Cat(nome="Armatura", tipo="ARMATURA")

session.add_all([equip_cat_arma, equip_cat_armatura])
session.commit()

# 🔹 5️⃣ Creazione Equipaggiamenti (10 Totali: 5 Armi, 5 Armature)
equipaggiamenti = [
    Equip(nome="Lancia del Drago", stats='{"attacco": 25}', categoria=equip_cat_arma),
    Equip(nome="Spada Gladiatore", stats='{"attacco": 20}', categoria=equip_cat_arma),
    Equip(nome="Verga del Fuoco", stats='{"magia": 30}', categoria=equip_cat_arma),
    Equip(nome="Bastone della Luce", stats='{"magia": 28}', categoria=equip_cat_arma),
    Equip(nome="Ascia Pesante", stats='{"attacco": 35}', categoria=equip_cat_arma),
    
    Equip(nome="Armatura di Mithril", stats='{"difesa": 20}', categoria=equip_cat_armatura),
    Equip(nome="Veste del Mago", stats='{"difesa": 15, "mana": 10}', categoria=equip_cat_armatura),
    Equip(nome="Scudo Sacro", stats='{"difesa": 25}', categoria=equip_cat_armatura),
    Equip(nome="Elmo del Drago", stats='{"difesa": 18}', categoria=equip_cat_armatura),
    Equip(nome="Mantello Oscuro", stats='{"evasione": 12}', categoria=equip_cat_armatura),
]

session.add_all(equipaggiamenti)
session.commit()

# 🔹 6️⃣ Creazione delle Abilità (10 Totali)
abilita = [
    # Abilità Attive
    Abilita(nome="Salto del Drago", p_ab=10, effect="DANNO"),
    Abilita(nome="Taglio Potente", p_ab=8, effect="DANNO"),
    Abilita(nome="Meteorite", p_ab=12, effect="DANNO"),
    Abilita(nome="Cura Suprema", p_ab=10, effect="CURA"),

    # Abilità Passive
    Abilita(nome="Pelle Dura", p_ab=0, effect="BUFF"),
    Abilita(nome="Magia Potenziata", p_ab=0, effect="BUFF"),

    # Abilità di Reazione
    Abilita(nome="Contrattacco", p_ab=0, effect="DANNO"),
    Abilita(nome="Risveglio Magico", p_ab=0, effect="BUFF"),

    # Abilità Innate (legate alla Razza)
    Abilita(nome="Forza Bangaa", p_ab=0, effect="BUFF"),
    Abilita(nome="Mana Innato", p_ab=0, effect="BUFF"),
]

session.add_all(abilita)
session.commit()

# 🔹 7️⃣ Associazione Abilità con Specializzazioni
session.add_all([
    Attiva(id=abilita[0].id),  # Salto del Drago
    Attiva(id=abilita[1].id),  # Taglio Potente
    Attiva(id=abilita[2].id),  # Meteorite
    Attiva(id=abilita[3].id),  # Cura Suprema

    Passiva(id=abilita[4].id),  # Pelle Dura
    Passiva(id=abilita[5].id),  # Magia Potenziata

    Reazione(id=abilita[6].id, trigger="DANNO_SUBITO"),  # Contrattacco
    Reazione(id=abilita[7].id, trigger="MAGIA"),  # Risveglio Magico

    Innata(id=abilita[8].id, trigger="BORN", razza=bangaa),  # Forza Bangaa
    Innata(id=abilita[9].id, trigger="BORN", razza=nu_mou),  # Mana Innato
])

session.commit()
session.close()

print("✅ Database popolato con successo!")
