from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import validates
from sqlalchemy.orm import relationship

Base = declarative_base()

######Stroj_Katalog TABLE
stroj_katalog_association = Table('stroj_katalog', Base.metadata,
                                  Column('stroj_id', Integer, ForeignKey('Stroj.stroj_id')),
                                  Column('katalog_stroju_id', Integer, ForeignKey('Katalog_stroju.katalog_stroju_id'))
                                  )


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

    katalogy = relationship("Katalog_stroju", secondary=stroj_katalog_association, back_populates="stroje")

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

    ######Katalog strojů TABLE


class Katalog_stroju(Base):
    __tablename__ = "Katalog_stroju"

    katalog_stroju_id = Column("katalog_stroju_id", Integer, primary_key=True, nullable=False)
    stroje = relationship("Stroj", secondary=stroj_katalog_association, back_populates="katalogy")

    def __init__(self, katalog_stroju_id):
        self.katalog_stroju_id = katalog_stroju_id

    def __repr__(self):
        return f"({self.katalog_stroju_id})"

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
        self.ucet_heslo = ucet_heslo
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

typ1 = Typ_stroje(1, "Typ1")
typ2 = Typ_stroje(2, "Typ2")

stroj1 = Stroj(stroj_id=1, stroj_nazev="Sekačka", stroj_cena=500.0, stroj_typ_id=1)
stroj2 = Stroj(stroj_id=2, stroj_nazev="Kombajn", stroj_cena=1500.0, stroj_typ_id=2)
katalog = Katalog_stroju(1)
katalog.stroje.extend([stroj1, stroj2])

dispecer = Ucet(2, "Franta", 1234, "franta@gmail.com", 1)
technik = Ucet(3, "Jirka", 1234, "jirka@gmail.com", 2)
zakaznik = Ucet(1, "Martin", 1234, "jirka@gmail.com", 3)
# session_maker.add(dispecer)
# session_maker.add(technik)
# session_maker.add(zakaznik)
pracovnik = Pracovnik(1, "Mirek", 150)

# session_maker.add(typ1)
# session_maker.add(typ2)
# session_maker.add(pracovnik)
# session_maker.add(katalog)
session_maker.commit()