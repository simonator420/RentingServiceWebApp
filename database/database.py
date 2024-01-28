from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash

Base = declarative_base()

######Pracovník(Kurýr) TABLE

class Pracovnik(Base):
    __tablename__ = "Pracovnik"

    pracovnik_id = Column("pracovnik_id", Integer, primary_key=True, nullable=False)
    pracovnik_jmeno = Column("pracovnik_jmeno", String, nullable=False)
    pracovnik_cena = Column("pracovnik_cena", Double, nullable=False)

    def __init__(self, pracovnik_id, pracovnik_jmeno, pracovnik_cena):
        self.pracovnik_id = pracovnik_id
        self.pracovnik_jmeno = pracovnik_jmeno
        self.pracovnik_cena = pracovnik_cena

    def __repr__(self):
        return f"({self.pracovnik_id}) {self.pracovnik_jmeno}, {self.pracovnik_cena}"


######Rezervace TABLE

class Rezervace(Base):
    __tablename__ = "Rezervace"

    rezervace_id = Column("rezervace_id", Integer, primary_key=True, nullable=False)
    # rezervace_platnost
    rezervace_platnost = Column("rezervace_platnost", Boolean, default=True, nullable=False)
    objednavka_id = Column("objednavka_id", Integer, ForeignKey("Objednavka.objednavka_id"), nullable=False)
    ucet_id = Column(Integer, ForeignKey('Ucet.ucet_id'))

    def __init__(self, rezervace_id, rezervace_platnost, objednavka_id, ucet_id):
        self.rezervace_id = rezervace_id
        self.rezervace_platnost = rezervace_platnost
        self.objednavka_id = objednavka_id
        self.ucet_id = ucet_id

    def __repr__(self):
        return f"({self.rezervace_id}) {self.rezervace_platnost}, {self.objednavka_id}"


######Objednavka TABLE

class Objednavka(Base):
    __tablename__ = "Objednavka"

    objednavka_id = Column("objednavka_id", Integer, primary_key=True, nullable=False)
    objednavka_datum_od = Column("objednavka_datum_od", Date, nullable=False)
    objednavka_datum_do = Column("objednavka_datum_do", Date, nullable=False)
    objednavka_zpracovana = Column("objednavka_zpracovana", Boolean, default=False)
    stroj_id = Column("stroj_id", Integer, ForeignKey("Stroj.stroj_id"), nullable=False)
    ucet_id = Column("ucet_id", Integer, ForeignKey("Ucet.ucet_id"), nullable=False)

    def __init__(self, objednavka_id, objednavka_datum_od, objednavka_datum_do, stroj_id, ucet_id):
        self.objednavka_id = objednavka_id
        self.objednavka_datum_od = objednavka_datum_od
        self.objednavka_datum_do = objednavka_datum_do
        self.stroj_id = stroj_id
        self.ucet_id = ucet_id

    def __repr__(self):
        return f"({self.objednavka_id}) {self.objednavka_datum_od}, {self.objednavka_datum_do}"


######Stroj TABLE

class Stroj(Base):
    __tablename__ = "Stroj"

    stroj_id = Column("stroj_id", Integer, primary_key=True, nullable=False)
    stroj_nazev = Column("stroj_nazev", String, nullable=False)
    stroj_cena = Column("stroj_cena", Float, nullable=False)
    typ_stroje_id = Column("typ_stroje_id", Integer, ForeignKey("Typ_stroje.typ_stroje_id"), nullable=False)

    def __init__(self, stroj_id, stroj_nazev, stroj_typ_id, stroj_cena):
        self.stroj_id = stroj_id
        self.stroj_nazev = stroj_nazev
        self.typ_stroje_id = stroj_typ_id
        self.stroj_cena = stroj_cena

    def __repr__(self):
        return f"({self.stroj_id}) {self.stroj_nazev},{self.stroj_typ_id}, {self.stroj_cena}"

    ######Typ stroje TABLE


class Typ_stroje(Base):
    __tablename__ = "Typ_stroje"

    typ_stroje_id = Column("typ_stroje_id", Integer, primary_key=True, nullable=False)
    typ_stroje_nazev = Column("typ_stroje_nazev", String, nullable=False)

    def __init__(self, typ_stroje_id, typ_stroje_nazev):
        self.typ_stroje_id = typ_stroje_id
        self.typ_stroje_nazev = typ_stroje_nazev

    def __repr__(self):
        return f"({self.typ_stroje_id}) {self.typ_stroje_nazev}"


######Zakazník TABLE


class Ucet(Base):
    __tablename__ = "Ucet"

    ucet_id = Column("ucet_id", Integer, primary_key=True, nullable=False)
    ucet_jmeno = Column("ucet_jmeno", String, nullable=False)
    ucet_heslo = Column("ucet_heslo", String, nullable=False)
    ucet_email = Column("ucet_email", String, nullable=False)
    typ_uctu_id = Column("typ_uctu_id", Integer, ForeignKey("Typ_uctu.typ_uctu_id"), nullable=False)

    def __init__(self, ucet_id, ucet_jmeno, ucet_heslo, ucet_email, typ_uctu_id):
        self.ucet_id = ucet_id
        self.ucet_jmeno = ucet_jmeno
        self.ucet_heslo = generate_password_hash(ucet_heslo)
        self.ucet_email = ucet_email
        self.typ_uctu_id = typ_uctu_id

    def __repr__(self):
        return f"({self.ucet_id}) {self.ucet_jmeno},{self.ucet_heslo}, {self.ucet_email}"


class Typ_uctu(Base):
    __tablename__ = "Typ_uctu"

    typ_uctu_id = Column("typ_uctu_id", Integer, primary_key=True, nullable=False)
    # Dispečer,Technik, Zákazník
    typ_uctu_nazev = Column("typ_uctu_nazev", String, nullable=False)

    def __init__(self, typ_uctu_id, typ_uctu_nazev, ucet_id):
        self.typ_uctu_id = typ_uctu_id
        self.typ_uctu_nazev = typ_uctu_nazev
        self.ucet_id = ucet_id

    def __repr__(self):
        return f"({self.zakaznik_id}) {self.zakaznik_jmeno}, {self.ucet_id}"


engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session_maker = Session()

# Prvotní nastavení testovacích účtu
# Neimplemntovano skrz SQL kvůli hashováni hesel
def add_user_if_not_exists(session, user_data):
    existing_user = session.query(Ucet).filter((Ucet.ucet_jmeno == user_data['ucet_jmeno']) |
                                               (Ucet.ucet_email == user_data['ucet_email'])).first()
    if existing_user is None:
        new_user = Ucet(
            ucet_id=user_data['ucet_id'],
            ucet_jmeno=user_data['ucet_jmeno'],
            ucet_heslo=user_data['ucet_heslo'],
            ucet_email=user_data['ucet_email'],
            typ_uctu_id=user_data['typ_uctu_id']
        )
        session.add(new_user)
        session.commit()
    else:
        print(f"User '{user_data['ucet_jmeno']}' already exists.")

users = [
    {"ucet_id": 1, "ucet_jmeno": "John_Dispecer", "ucet_heslo": "dispecer123", "ucet_email": "john.dispecer@example.com", "typ_uctu_id": 1},
    {"ucet_id": 2, "ucet_jmeno": "Jane_Technik", "ucet_heslo": "technik123", "ucet_email": "jane.technik@example.com", "typ_uctu_id": 2},
    {"ucet_id": 3, "ucet_jmeno": "Bob_Zakaznik", "ucet_heslo": "zakaznik123", "ucet_email": "bob.zakaznik@example.com", "typ_uctu_id": 3}
]

for user_data in users:
    add_user_if_not_exists(session_maker, user_data)

session_maker.commit()