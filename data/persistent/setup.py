from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Enum, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uuid
from functools import wraps
from sqlalchemy import event
from sqlalchemy.orm import validates
import enum

# Creaction del database SQLite con SQLAlchemy
DATABASE_URL = "sqlite:///persistent.db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

def generate_id(mapper, connection, target):
    """Genera un ID basato sul name e la tabella prima dell'inserimento"""
    if hasattr(target, "name"):  # Assicuriamoci che la classs abbia un campo 'name'
        clean_name = target.name.lower().replace(" ", "_")
        target.id = f"{clean_name}__{target.__tablename__}"

# Registriamo l'evento per tutte le classi che hanno una tabella
def register_listeners():
    for mapper in Base.registry.mappers:
        cls = mapper.class_
        if hasattr(cls, "__tablename__") and hasattr(cls, "id"):
            event.listen(cls, "before_insert", generate_id)

class Race(Base):
    __tablename__ = "race"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    innate_abilities = relationship("Innate", back_populates="race")

# 2️⃣ Classs

class Classs(Base):
    __tablename__ = "classs"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    requisiti = Column(String)  # Può essere JSON

# Tabella ponte Race <-> Classs (N:N)
Race_Classs = Table(
    "race_classs", Base.metadata,
    Column("race_id", String, ForeignKey("race.id", ondelete="CASCADE"), primary_key=True),
    Column("classs_id", String, ForeignKey("classs.id", ondelete="CASCADE"), primary_key=True)
)
class TriggerEnum(enum.Enum):
    ONE = 1
    TWO = 2
# 3️⃣ Equipaggiamento
class Equip_Cat(Base):
    __tablename__ = "equip_cat"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(Enum("TORSO", "HEAD", "BOOTS", "WEAPON", "SHIELD","ACCESSORY", name="trigger_enum"), nullable=True)
    slot = Column(Enum(TriggerEnum, name="trigger_enum"), default=TriggerEnum.ONE)
    misc = Column(String)
    equip_items = relationship("Equip", back_populates="category")


class Equip(Base):
    __tablename__ = "equip"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    stats = Column(String, nullable=False)  # Può essere JSON
    equip_cat_id = Column(String, ForeignKey("equip_cat.id", ondelete="CASCADE"), nullable=False)
    category = relationship("Equip_Cat", back_populates="equip_items")

# Tabella ponte Classs <-> Equip_Cat (N:N)
Classs_Equip_Cat = Table(
    "classs_equip_cat", Base.metadata,
    Column("classs_id", String, ForeignKey("classs.id", ondelete="CASCADE"), primary_key=True),
    Column("equip_cat_id", String, ForeignKey("equip_cat.id", ondelete="CASCADE"), primary_key=True)
)

# 4️⃣ Abilità

class Skill(Base):
    __tablename__ = "skill"
    id = Column(String, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    type = Column(Enum("ACTIVE","PASSIVE","INNATE","REACTION","HIDDEN", name="trigger_enum"), nullable=False)
    trigger = Column(Enum("DAMAGE_RECEIVED", "ATTACK", "MAGIC", "MOVE", name="trigger_enum"), nullable=True)
    p_ab = Column(Integer, nullable=False)
    family = Column(Enum("PHY", "MAG", name="type_enum"), nullable=False)
    effect = Column(Enum("DAMAGE", "HEAL", "BUFF", "DEBUFF", name="effect_enum"), nullable=False)

    @validates("trigger")
    def validate_trigger(self, key, value):
        """Assicura che trigger sia valorizzato solo se type = 'REACTION'"""
        if (self.type == "ACTIVE") and value is not None:
            raise ValueError("Trigger no può essere impostato solo se type = 'ACTIVE'")
        if self.type == "REACTION" and value is None:
            raise ValueError("Se type è 'REACTION', il trigger deve essere specificato")
        return value
# Tabella ponte Equip <-> Skill (N:N)
Equip_Skill = Table(
    "equip_skill", Base.metadata,
    Column("equip_id", String, ForeignKey("equip.id", ondelete="CASCADE"), primary_key=True),
    Column("skill_id", String, ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)
)

# 5️⃣ Specializzazione Abilità (Ereditarietà 1:1)

class Active(Base):
    __tablename__ = "active"
    id = Column(String, ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)


class Passive(Base):
    __tablename__ = "passive"
    id = Column(String, ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)


class Reaction(Base):
    __tablename__ = "reaction"
    id = Column(String, ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)
    trigger = Column(Enum("DAMAGE_RECEIVED", "ATTACK", "MAGIC", "MOVE", name="trigger_enum"), nullable=False)


class Innate(Base):
    __tablename__ = "innate"
    id = Column(String, ForeignKey("skill.id", ondelete="CASCADE"), primary_key=True)
    trigger = Column(Enum("BORN", "LEVEL_UP", "EVOLVE", name="trigger_enum"), nullable=False)
    race_id = Column(String, ForeignKey("race.id", ondelete="CASCADE"), nullable=False)
    race = relationship("Race", back_populates="innate_abilities")

# Creaction delle tabelle
Base.metadata.create_all(engine)


# Chiamata per registrare i listener dopo la definizione delle classi
register_listeners()
# Creaction della sessione

# Creaction della sessione
Session = sessionmaker(bind=engine)
session = Session()

# Creaction delle razze
bangaa = Race(name="Bangaa")
nu_mou = Race(name="Nu Mou")
session.add_all([bangaa, nu_mou])
session.commit()

# Creaction delle classi
black_mage = Classs(name="Black Mage")
white_mage = Classs(name="White Mage")
dragoon = Classs(name="Dragoon")
gladiator = Classs(name="Gladiator")
session.add_all([black_mage, white_mage, dragoon, gladiator])
session.commit()

# Associazione delle classi alle razze nella tabella ponte
session.execute(Race_Classs.insert().values(race_id=nu_mou.id, classs_id=black_mage.id))
session.execute(Race_Classs.insert().values(race_id=nu_mou.id, classs_id=white_mage.id))
session.execute(Race_Classs.insert().values(race_id=bangaa.id, classs_id=dragoon.id))
session.execute(Race_Classs.insert().values(race_id=bangaa.id, classs_id=gladiator.id))
session.commit()

# Creaction delle categorie di equipaggiamento
sword = Equip_Cat(type="WEAPON",name="Sword",misc='{"range":1}')
bow = Equip_Cat(type="WEAPON",name="Bow",misc='{"range":5}')
spear = Equip_Cat(type="WEAPON",name="Spear",misc='{"range":2}')
greatsword = Equip_Cat(type="WEAPON",name="Greatsword",slot=TriggerEnum.TWO,misc='{"range":1}')
wand = Equip_Cat(type="WEAPON",name="Wand",slot=TriggerEnum.TWO,misc='{"range":5}')

armor = Equip_Cat(type="TORSO",name="Armor")
waist = Equip_Cat(type="TORSO",name="Waist")

helm = Equip_Cat(type="HEAD", name="Helm")
hat = Equip_Cat(type="HEAD", name="Hat")

ring = Equip_Cat(type="ACCESSORY", name="ring")

session.add_all([sword, bow, spear, greatsword, armor, waist, helm, hat, ring, wand])
session.commit()

# Creaction degli equipaggiamenti
equip_list = [

    Equip(name="Firebrand", stats='{"atk": 10, "fire": 5}', equip_cat_id=greatsword.id),
    Equip(name="Bastone del Fulmine", stats='{"atk": 8, "thunder": 5}', equip_cat_id=wand.id),
    Equip(name="Lancia del Drago", stats='{"atk": 12, "piercing": 7}', equip_cat_id=spear.id),
    Equip(name="Spada da Guerra", stats='{"atk": 15, "stun": 5}', equip_cat_id=sword.id),

    Equip(name="Armatura Pesante", stats='{"def": 10, "res": 5}', equip_cat_id=armor.id),
    Equip(name="Veste Magica", stats='{"def": 5, "mp": 10}', equip_cat_id=waist.id),
    Equip(name="Cotta di Maglia", stats='{"def": 7, "agi": 3}', equip_cat_id=armor.id),
    Equip(name="Mantello Stregato", stats='{"def": 4, "magic_def": 10}', equip_cat_id=waist.id),
    Equip(name="Helm del Cavaliere", stats='{"def": 6, "hp": 10}', equip_cat_id=helm.id),
    Equip(name="Cappello dello Stregone", stats='{"def": 3, "mp": 8}', equip_cat_id=hat.id),
    Equip(name="Corno del Dragone", stats='{"def": 5, "atk": 3}', equip_cat_id=helm.id),
    Equip(name="Corona del Re", stats='{"def": 4, "leadership": 5}', equip_cat_id=hat.id),
]

session.add_all(equip_list)
session.commit()

# Creaction delle abilità
skill_list = [
    Skill(name="Palla di Fuoco", p_ab=5, effect="DAMAGE", type="ACTIVE", family="MAG"),
    Skill(name="Fulmine", p_ab=4, effect="DAMAGE", type="ACTIVE", family="MAG"),
    Skill(name="Cura", p_ab=3, effect="HEAL", type="ACTIVE", family="MAG"),
    Skill(name="Rigene", p_ab=2, effect="BUFF", type="ACTIVE", family="MAG"),
    Skill(name="Corace", p_ab=3, effect="BUFF", type="ACTIVE", family="MAG"),
    Skill(name="Avvelenamento", p_ab=4, effect="DEBUFF", type="ACTIVE", family="MAG"),
    Skill(name="Attacco Rapido", p_ab=3, effect="DAMAGE", type="ACTIVE", family="PHY"),
    Skill(name="Difesa Totale", p_ab=3, effect="BUFF", type="ACTIVE", family="MAG"),
    Skill(name="Sfera Oscura", p_ab=6, effect="DAMAGE", type="ACTIVE", family="MAG"),
    Skill(name="Lama della Tempesta", p_ab=5, effect="DAMAGE", type="ACTIVE", family="PHY"),
]

session.add_all(skill_list)
session.commit()

# Associazione tra equipaggiamento e abilità
session.execute(Equip_Skill.insert().values(equip_id=equip_list[0].id, skill_id=skill_list[0].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[1].id, skill_id=skill_list[1].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[2].id, skill_id=skill_list[6].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[3].id, skill_id=skill_list[9].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[4].id, skill_id=skill_list[4].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[5].id, skill_id=skill_list[2].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[6].id, skill_id=skill_list[7].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[7].id, skill_id=skill_list[8].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[8].id, skill_id=skill_list[5].id))
session.execute(Equip_Skill.insert().values(equip_id=equip_list[9].id, skill_id=skill_list[3].id))

session.commit()

# Associare le categorie di equipaggiamento alle classi
session.execute(Classs_Equip_Cat.insert().values(classs_id=black_mage.id, equip_cat_id=hat.id))
session.execute(Classs_Equip_Cat.insert().values(classs_id=white_mage.id, equip_cat_id=hat.id))

session.execute(Classs_Equip_Cat.insert().values(classs_id=dragoon.id, equip_cat_id=greatsword.id))
session.execute(Classs_Equip_Cat.insert().values(classs_id=dragoon.id, equip_cat_id=helm.id))

session.execute(Classs_Equip_Cat.insert().values(classs_id=gladiator.id, equip_cat_id=bow.id))
session.execute(Classs_Equip_Cat.insert().values(classs_id=gladiator.id, equip_cat_id=sword.id))
session.execute(Classs_Equip_Cat.insert().values(classs_id=gladiator.id, equip_cat_id=helm.id))



session.commit()

# Chiusura della sessione
session.close()