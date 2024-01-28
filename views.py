from flask import *
from forms import *
from database.database import *
from markupsafe import Markup
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import datetime


views = Blueprint(__name__, 'views')
click=0

#Hlavní stránka při prvním načtení
@views.route('/index.html')
def homer():
    return render_template('index.html')


#Hlavní stránka
@views.route('/', methods=['GET', 'POST'], endpoint='home')
def home():
    form = ObjednavkaForm()
    results = []

    # Kontrola, zda byl formulář odeslán
    if form.is_submitted():
        typ = form.typ.data
        datum_od = form.datum_od.data
        datum_do = form.datum_do.data

        # Vytvoření dotazu do databáze na základě zadaných údajů
        query = (
            session_maker.query(Stroj)
            .join(Typ_stroje, Typ_stroje.typ_stroje_id == Stroj.typ_stroje_id)
            .filter(
                Typ_stroje.typ_stroje_nazev == typ,
            )
        )

        # Získání výsledků dotazu
        results = query.all()

    # Vrátí šablonu index.html s předanými daty
    return render_template('index.html', form=form, results=results)


#O nás
@views.route('/o-nas')
def onas():
    return render_template('index.html', target_section='o-nas')

#Výpis strojů
@views.route('/nabidka-stroju', methods=['GET', 'POST'])
def nabidka_stroju():
    if request.method == 'POST':
        # Zpracování formuláře pro výběr a objednání stroje
        if 'stroj_id' in request.form:
            # Získání dat z formuláře
            stroj_id = request.form['stroj_id']
            datum_od_str = request.form['datum_od']
            datum_do_str = request.form['datum_do']
            ucet_id = request.form['ucet_id']

            datum_od = datetime.datetime.strptime(datum_od_str, '%Y-%m-%d').date()
            datum_do = datetime.datetime.strptime(datum_do_str, '%Y-%m-%d').date()

            # Vytvoření nové objednávky
            new_objednavka = Objednavka(
                objednavka_id = None,
                objednavka_datum_od = datum_od,
                objednavka_datum_do = datum_do,
                stroj_id = stroj_id,
                ucet_id=ucet_id
            )

            # Přidání objednávky do databáze a potvrzení
            session_maker.add(new_objednavka)
            session_maker.commit()

        # Filtrování strojů podle zvoleného typu
        selected_type = request.form.get('machine-type')
        if selected_type and selected_type != 'default':
            stroje = session_maker.query(Stroj).join(Typ_stroje).filter(Typ_stroje.typ_stroje_id == int(selected_type)).all()
        else:
            stroje = session_maker.query(Stroj).all()

    else:
        stroje = session_maker.query(Stroj).all()

    # Vrátí šablonu nabidka-stroju.html s daty o strojích
    return render_template('nabidka-stroju.html', stroje=stroje)

#Výpis pracovníků
@views.route('/pracovnici')
def pracovnici():
    pracovnici = session_maker.query(Pracovnik).all()
    return render_template('pracovnici.html', pracovnici=pracovnici)

#Přihlášení zákazníka
@views.route('/prihlaseni', methods=['GET', 'POST'])
def prihlaseni():
    form_prihlaseni = SingupForm()

    # Zpracování formuláře po odeslání
    if request.method == 'POST' and form_prihlaseni.validate_on_submit():
        # Získání uživatelského jména a hesla z formuláře
        jmeno = form_prihlaseni.name.data
        heslo = form_prihlaseni.password.data

        # Hledání účtu v databázi
        ucet = session_maker.query(Ucet).filter_by(ucet_jmeno=jmeno).first()

        # Ověření hesla a přihlášení uživatele
        if ucet and check_password_hash(ucet.ucet_heslo, heslo):
            # Nastavení session proměnných
            session['user_name'] = jmeno
            session['ucet_id'] = ucet.ucet_id
            session['typ_uctu_id'] = ucet.typ_uctu_id
            print('Úspěšně přihlášen')
            # Přesměrování na domovskou stránku
            return redirect(url_for('views.home'))
        else:
            print('Nesprávné uživatelské jméno nebo heslo')

    # Vrátí šablonu prihlaseni.html s formulářem pro přihlášení
    return render_template('prihlaseni.html', form=form_prihlaseni)

#Registrace zákazníka
@views.route('/registrace', methods=['GET', 'POST'])
def registrace():
    form = RegisterForm()

    # Zpracování formuláře po odeslání
    if request.method == 'POST' and form.validate_on_submit():
        # Získání údajů z formuláře
        name = form.name.data
        email = form.email.data
        password = form.password.data

        # hashed_password = generate_password_hash(password)

        # Vytvoření nového účtu
        ucet_count = session_maker.query(Ucet).count()
        new_ucet_id = ucet_count + 1
        new_ucet = Ucet(new_ucet_id, ucet_jmeno=name, ucet_email=email, ucet_heslo=password, typ_uctu_id=3)

        # Přidání účtu do databáze a potvrzení
        session_maker.add(new_ucet)
        session_maker.commit()

        # Přesměrování na stránku pro přihlášení
        return redirect(url_for('views.prihlaseni'))

    # Vrátí šablonu registrace.html s formulářem pro registraci
    return render_template('registrace.html', form=form)

#Odhlášení zákazníka
@views.route('/odhlaseni')
def odhlaseni():
    # Vyčištění session proměnných
    session.clear()
    # Přesměrování na domovskou stránku
    return redirect(url_for('views.home'))

# Získání objednávek do obou tabulek na stránce objednavky-k-potvrzeni
@views.route('/objednavky-k-potvrzeni')
def objednavky_k_potvrzeni():
    # Dotaz do databáze pro získání všech objednávek
    objednavky = session_maker.query(Objednavka).all()

    # Získání ID objednávek s neplatnou rezervací
    zrusene_rezervace_id = [rez.objednavka_id for rez in session_maker.query(Rezervace).filter_by(rezervace_platnost=False).all()]

    # Vrátí šablonu objednavky-k-potvrzeni.html s daty o objednávkách
    return render_template('objednavky-k-potvrzeni.html', objednavky=objednavky, zrusene_rezervace=zrusene_rezervace_id)

# Získání seznamu všech pracovníků (techniku)
@views.route('/get-pracovnici')
def get_pracovnici():
    # Dotaz do databáze pro získání všech účtů s typem pracovník
    ucet_records = session_maker.query(Ucet).filter(Ucet.typ_uctu_id == 2).all()
    return jsonify([{ 'ucet_id': ucet.ucet_id, 'ucet_jmeno': ucet.ucet_jmeno } for ucet in ucet_records])


# Vytvoření nového záznamu do tabulky Rezervace po přiřazení pracovníka dispečerem
@views.route('/vytvorit_rezervaci', methods=['POST'])
def vytvorit_rezervaci():
    # Přijetí JSON dat z požadavku
    data = request.json
    objednavka_id = data['objednavka_id']
    ucet_id = data['ucet_ids'][0]

    # Vytvoření nové rezervace
    new_rezervace = Rezervace(
        rezervace_id=None,
        rezervace_platnost=True,
        objednavka_id=objednavka_id,
        ucet_id=ucet_id
    )

    # Aktualizace stavu objednávky
    objednavka = session_maker.query(Objednavka).filter_by(objednavka_id=objednavka_id).first()
    if objednavka:
        objednavka.objednavka_zpracovana = True
        session_maker.commit()

    # Přidání rezervace do databáze
    session_maker.add(new_rezervace)
    session_maker.commit()

    # Vrátí potvrzení o úspěšném vytvoření rezervace ve formátu JSON
    return jsonify({'message': 'Rezervace uspesne vytvorena'})


# Vypisování potvrzených rezervací na stránce profil.html
@views.route('/profil')
def profil():
    # Získání ID přihlášeného uživatele
    user_id = session.get('ucet_id')

    # Zpracování pouze pokud je uživatel přihlášen
    if user_id is not None:
        # Dotaz do databáze pro získání rezervací přihlášeného uživatele
        rezervace_zaznamy = session_maker.query(
            Rezervace,
            Objednavka.objednavka_datum_od,
            Objednavka.objednavka_datum_do,
            Stroj.stroj_nazev, Stroj.stroj_cena,
            Ucet.ucet_jmeno
        ).join(Objednavka, Rezervace.objednavka_id == Objednavka.objednavka_id) \
            .join(Stroj, Objednavka.stroj_id == Stroj.stroj_id) \
            .join(Ucet, Rezervace.ucet_id == Ucet.ucet_id) \
            .filter(Objednavka.ucet_id == user_id).all()

        # Výpočet celkové ceny za každou rezervaci
        zpracovane_zaznamy = []
        for zaznam in rezervace_zaznamy:
            hours = (zaznam[2] - zaznam[1]).total_seconds() / 3600
            fixed_cost = 150
            cena = int(zaznam[4] * hours + fixed_cost * hours)
            zpracovany_zaznam = tuple(zaznam) + (cena,)
            zpracovane_zaznamy.append(zpracovany_zaznam)

        # Vrátí šablonu profil.html s daty rezervací
        return render_template('profil.html', rezervace_records=zpracovane_zaznamy)

    # Přesměrování na přihlášení, pokud uživatel není přihlášen
    return redirect(url_for('views.prihlaseni'))

# Zrušení rezervace uživatelem
@views.route('/zrusit_rezervaci', methods=['POST'])
def zrusit_rezervaci():
    # Získání ID rezervace z formuláře
    rezervace_id = request.form.get('rezervace_id')

    # Dotaz do databáze pro nalezení specifické rezervace
    rezervace_to_cancel = session_maker.query(Rezervace).filter_by(rezervace_id=rezervace_id).first()

    # Pokud byla rezervace nalezena, nastaví se jako neplatná
    if rezervace_to_cancel:
        # Po stisknuti tlačítka se rezervace oznaci jako False
        rezervace_to_cancel.rezervace_platnost = False
        session_maker.commit()

    # Přesměrování zpět na profil uživatele
    return redirect(url_for('views.profil'))

# Zrušení objednávky dispečerem
@views.route('/zrusit_objednavku', methods=['POST'])
def zrusit_objednavku():
    # Získání ID objednávky z formuláře
    objednavka_id = request.form.get('objednavka_id')

    # Vyhledání a vymazání příslušné rezervace
    rezervace_to_delete = session_maker.query(Rezervace).filter_by(objednavka_id=objednavka_id).first()
    if rezervace_to_delete:
        session_maker.delete(rezervace_to_delete)

    # Vyhledání a vymazání objednávky
    objednavka_to_delete = session_maker.query(Objednavka).filter_by(objednavka_id=objednavka_id).first()
    if objednavka_to_delete:
        session_maker.delete(objednavka_to_delete)

    session_maker.commit()

    # Přesměrování na stránku s objednávkami k potvrzení
    return redirect(url_for('views.objednavky_k_potvrzeni'))

# Zobrazení zakázek přihlášeného uživatele
@views.route('/moje-zakazky')
def moje_zakazky():
    # Získání ID přihlášeného uživatele
    user_id = session.get('ucet_id')

    # Dotaz do databáze pro získání rezervací daného uživatele
    rezervace_zaznamy = session_maker.query(
        Rezervace.rezervace_id,
        Objednavka.objednavka_datum_od,
        Objednavka.objednavka_datum_do,
        Stroj.stroj_nazev
    ).join(Objednavka, Rezervace.objednavka_id == Objednavka.objednavka_id) \
     .join(Stroj, Objednavka.stroj_id == Stroj.stroj_id) \
     .filter(Rezervace.ucet_id == user_id).all()

    # Vrátí šablonu moje-zakazky.html s daty o rezervacích
    return render_template('moje-zakazky.html', rezervace_records=rezervace_zaznamy)

