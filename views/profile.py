from flask import *
from forms.forms import *
from database.database import *
from werkzeug.security import check_password_hash
import datetime


profile = Blueprint('profile', __name__)

#Přihlášení zákazníka
@profile.route('/prihlaseni', methods=['GET', 'POST'])
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
            return redirect(url_for('homepage.home'))
        else:
            print('Nesprávné uživatelské jméno nebo heslo')

    # Vrátí šablonu prihlaseni.jinja s formulářem pro přihlášení
    return render_template('profile/prihlaseni.jinja', form=form_prihlaseni)

#Registrace zákazníka
@profile.route('/registrace', methods=['GET', 'POST'])
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
        return redirect(url_for('profile.prihlaseni'))

    # Vrátí šablonu registrace.jinja s formulářem pro registraci
    return render_template('profile/registrace.jinja', form=form)

#Odhlášení zákazníka
@profile.route('/odhlaseni')
def odhlaseni():
    # Vyčištění session proměnných
    session.clear()
    # Přesměrování na domovskou stránku
    return redirect(url_for('homepage.home'))

# Vypisování potvrzených rezervací na stránce profil.jinja
@profile.route('/profil')
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

        # Vrátí šablonu profil.jinja s daty rezervací
        return render_template('profile/profil.jinja', rezervace_records=zpracovane_zaznamy)

    # Přesměrování na přihlášení, pokud uživatel není přihlášen
    return redirect(url_for('profile.prihlaseni'))

#Výpis pracovníků
@profile.route('/pracovnici')
def pracovnici():
    pracovnici = session_maker.query(Pracovnik).all()
    return render_template('pracovnici.html', pracovnici=pracovnici)

# Získání seznamu všech pracovníků (techniku)
@profile.route('/get-pracovnici')
def get_pracovnici():
    # Dotaz do databáze pro získání všech účtů s typem pracovník
    ucet_records = session_maker.query(Ucet).filter(Ucet.typ_uctu_id == 2).all()
    return jsonify([{ 'ucet_id': ucet.ucet_id, 'ucet_jmeno': ucet.ucet_jmeno } for ucet in ucet_records])
