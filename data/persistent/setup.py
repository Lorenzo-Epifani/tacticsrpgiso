from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Enum, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uuid
from functools import wraps
from sqlalchemy import event
from sqlalchemy.orm import validates

# Creazione del database SQLite con SQLAlchemy
DATABASE_URL = "sqlite:///persistent.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

def generate_id(mapper, connection, target):
    """Genera un ID basato sul nome e la tabella prima dell'inserimento"""
    if hasattr(target, "nome"):  # Assicuriamoci che la classe abbia un campo 'nome'
        clean_name = target.nome.lower().replace(" ", "_")
        target.id = f"{clean_name}__{target.__tablename__}"

# Registriamo l'evento per tutte le classi che hanno una tabella
def register_listeners():
    for mapper in Base.registry.mappers:
        cls = mapper.class_
        if hasattr(cls, "__tablename__") and hasattr(cls, "id"):
            event.listen(cls, "before_insert", generate_id)

class Razza(Base):
    __tablename__ = "razza"
    id = Column(String, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    innate_abilities = relationship("Innata", back_populates="razza")

# 2️⃣ Classe

class Classe(Base):
    __tablename__ = "classe"
    id = Column(String, primary_key=True)
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
    id = Column(String, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    equip_items = relationship("Equip", back_populates="categoria")


class Equip(Base):
    __tablename__ = "equip"
    id = Column(String, primary_key=True)
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
    id = Column(String, primary_key=True)
    nome = Column(String, unique=True, nullable=False)
    tipo = Column(Enum("ATTIVA","PASSIVA","INNATA","REAZIONE","NASCOSTA", name="trigger_enum"), nullable=False)
    trigger = Column(Enum("DANNO_SUBITO", "ATTACCO", "MAGIA", "MOVIMENTO", name="trigger_enum"), nullable=True)
    p_ab = Column(Integer, nullable=False)
    effect = Column(Enum("DANNO", "CURA", "BUFF", "DEBUFF", name="effect_enum"), nullable=False)

    @validates("trigger")
    def validate_trigger(self, key, value):
        """Assicura che trigger sia valorizzato solo se tipo = 'REAZIONE'"""
        if (self.tipo == "ATTIVA") and value is not None:
            raise ValueError("Trigger no può essere impostato solo se tipo = 'ATTIVA'")
        if self.tipo == "REAZIONE" and value is None:
            raise ValueError("Se tipo è 'REAZIONE', il trigger deve essere specificato")
        return value
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


# Chiamata per registrare i listener dopo la definizione delle classi
register_listeners()
# Creazione della sessione

# Creazione della sessione
Session = sessionmaker(bind=engine)
session = Session()

# Creazione delle razze
bangaa = Razza(nome="Bangaa")
nu_mou = Razza(nome="Nu Mou")
session.add_all([bangaa, nu_mou])
session.commit()

# Creazione delle classi
mago_nero = Classe(nome="Mago Nero")
mago_bianco = Classe(nome="Mago Bianco")
dragone = Classe(nome="Dragone")
gladiatore = Classe(nome="Gladiatore")
session.add_all([mago_nero, mago_bianco, dragone, gladiatore])
session.commit()

# Associazione delle classi alle razze nella tabella ponte
session.execute(Razza_Classe.insert().values(razza_id=nu_mou.id, classe_id=mago_nero.id))
session.execute(Razza_Classe.insert().values(razza_id=nu_mou.id, classe_id=mago_bianco.id))
session.execute(Razza_Classe.insert().values(razza_id=bangaa.id, classe_id=dragone.id))
session.execute(Razza_Classe.insert().values(razza_id=bangaa.id, classe_id=gladiatore.id))
session.commit()

# Creazione delle categorie di equipaggiamento
arma = Equip_Cat(nome="Arma")
armatura = Equip_Cat(nome="Armatura")
elmo = Equip_Cat(nome="Elmo")
session.add_all([arma, armatura, elmo])
session.commit()

# Creazione degli equipaggiamenti
equip_list = [
    Equip(nome="Spada del Fuoco", stats='{"atk": 10, "fire": 5}', equip_cat_id=arma.id),
    Equip(nome="Bastone del Fulmine", stats='{"atk": 8, "thunder": 5}', equip_cat_id=arma.id),
    Equip(nome="Lancia del Drago", stats='{"atk": 12, "piercing": 7}', equip_cat_id=arma.id),
    Equip(nome="Martello da Guerra", stats='{"atk": 15, "stun": 5}', equip_cat_id=arma.id),
    Equip(nome="Armatura Pesante", stats='{"def": 10, "res": 5}', equip_cat_id=armatura.id),
    Equip(nome="Veste Magica", stats='{"def": 5, "mp": 10}', equip_cat_id=armatura.id),
    Equip(nome="Cotta di Maglia", stats='{"def": 7, "agi": 3}', equip_cat_id=armatura.id),
    Equip(nome="Mantello Stregato", stats='{"def": 4, "magic_def": 10}', equip_cat_id=armatura.id),
    Equip(nome="Elmo del Cavaliere", stats='{"def": 6, "hp": 10}', equip_cat_id=elmo.id),
    Equip(nome="Cappello dello Stregone", stats='{"def": 3, "mp": 8}', equip_cat_id=elmo.id),
    Equip(nome="Corno del Dragone", stats='{"def": 5, "atk": 3}', equip_cat_id=elmo.id),
    Equip(nome="Corona del Re", stats='{"def": 4, "leadership": 5}', equip_cat_id=elmo.id),
]

session.add_all(equip_list)
session.commit()

# Creazione delle abilità
abilita_list = [
    Abilita(nome="Palla di Fuoco", p_ab=5, effect="DANNO", tipo="ATTIVA"),
    Abilita(nome="Fulmine", p_ab=4, effect="DANNO", tipo="ATTIVA"),
    Abilita(nome="Cura", p_ab=3, effect="CURA", tipo="ATTIVA"),
    Abilita(nome="Rigene", p_ab=2, effect="BUFF", tipo="ATTIVA"),
    Abilita(nome="Corazza", p_ab=3, effect="BUFF", tipo="ATTIVA"),
    Abilita(nome="Avvelenamento", p_ab=4, effect="DEBUFF", tipo="ATTIVA"),
    Abilita(nome="Attacco Rapido", p_ab=3, effect="DANNO", tipo="ATTIVA"),
    Abilita(nome="Difesa Totale", p_ab=3, effect="BUFF", tipo="ATTIVA"),
    Abilita(nome="Sfera Oscura", p_ab=6, effect="DANNO", tipo="ATTIVA"),
    Abilita(nome="Lama della Tempesta", p_ab=5, effect="DANNO", tipo="ATTIVA"),
]

session.add_all(abilita_list)
session.commit()

# Associazione tra equipaggiamento e abilità
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[0].id, abilita_id=abilita_list[0].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[1].id, abilita_id=abilita_list[1].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[2].id, abilita_id=abilita_list[6].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[3].id, abilita_id=abilita_list[9].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[4].id, abilita_id=abilita_list[4].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[5].id, abilita_id=abilita_list[2].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[6].id, abilita_id=abilita_list[7].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[7].id, abilita_id=abilita_list[8].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[8].id, abilita_id=abilita_list[5].id))
session.execute(Equip_Abilita.insert().values(equip_id=equip_list[9].id, abilita_id=abilita_list[3].id))

session.commit()

# Associare le categorie di equipaggiamento alle classi
session.execute(Classe_Equip_Cat.insert().values(classe_id=mago_nero.id, equip_cat_id=arma.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=mago_bianco.id, equip_cat_id=arma.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=dragone.id, equip_cat_id=arma.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=gladiatore.id, equip_cat_id=arma.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=mago_nero.id, equip_cat_id=armatura.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=mago_bianco.id, equip_cat_id=armatura.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=dragone.id, equip_cat_id=armatura.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=gladiatore.id, equip_cat_id=armatura.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=dragone.id, equip_cat_id=elmo.id))
session.execute(Classe_Equip_Cat.insert().values(classe_id=gladiatore.id, equip_cat_id=elmo.id))

session.commit()

# Chiusura della sessione
session.close()