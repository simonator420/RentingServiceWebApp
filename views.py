from flask import *
from forms import *
from database.database import *
from markupsafe import Markup
from werkzeug.utils import secure_filename
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
    results = []  # List to store results

    if form.is_submitted():
        typ = form.typ.data
        datum_od = form.datum_od.data
        datum_do = form.datum_do.data

        query = (
            session_maker.query(Stroj)
            .join(Typ_stroje, Typ_stroje.typ_stroje_id == Stroj.typ_stroje_id)
            .filter(
                Typ_stroje.typ_stroje_nazev == typ,
            )
        )

        results = query.all()

    return render_template('index.html', form=form, results=results)


#O nás
@views.route('/o-nas')
def onas():
    return render_template('index.html', target_section='o-nas')

#Výpis strojů
#Výpis strojů
@views.route('/nabidka-stroju', methods=['GET', 'POST'])
def nabidka_stroju():
    if request.method == 'POST':
        # Check if this is a form submission for creating an Objednavka
        if 'stroj_id' in request.form:
            stroj_id = request.form['stroj_id']
            datum_od_str = request.form['datum_od']
            datum_do_str = request.form['datum_do']
            ucet_id = request.form['ucet_id']

            # Convert string dates to Python date objects
            datum_od = datetime.datetime.strptime(datum_od_str, '%Y-%m-%d').date()
            datum_do = datetime.datetime.strptime(datum_do_str, '%Y-%m-%d').date()

            new_objednavka = Objednavka(
                objednavka_id = None,  # Assuming autoincrement is enabled
                objednavka_datum_od = datum_od,
                objednavka_datum_do = datum_do,
                stroj_id = stroj_id,
                ucet_id=ucet_id
            )
            session_maker.add(new_objednavka)
            session_maker.commit()

        # After processing the form submission, continue to load the machines
        selected_type = request.form.get('machine-type')

        if selected_type and selected_type != 'default':
            stroje = session_maker.query(Stroj).join(Typ_stroje).filter(Typ_stroje.typ_stroje_id == int(selected_type)).all()
        else:
            stroje = session_maker.query(Stroj).all()

    else:
        stroje = session_maker.query(Stroj).all()

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

    if request.method == 'POST' and form_prihlaseni.validate_on_submit():
        jmeno = form_prihlaseni.name.data  # Accessing the username from the form
        heslo = form_prihlaseni.password.data  # Accessing the password from the form

        # Hledani uceta v databazi
        ucet = session_maker.query(Ucet).filter_by(ucet_jmeno=jmeno, ucet_heslo=heslo).first()

        if ucet:
            # Ziskání jména pro funkci set_user_name() pro jeho vypsání v záhlaví
            session['user_name'] = jmeno
            session['ucet_id'] = ucet.ucet_id
            # Ziskání jména pro funkci set_typ_uctu_id() pro nastavení stránek v záhlaví
            session['typ_uctu_id'] = ucet.typ_uctu_id
            print('Úspěšně přihlášen')
            return redirect(url_for('views.home'))
        else:
            print('Nesprávné uživatelské jméno nebo heslo')

    return render_template('prihlaseni.html', form=form_prihlaseni)

#Registrace zákazníka
@views.route('/registrace', methods=['GET', 'POST'])
def registrace():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        ucet_count = session_maker.query(Ucet).count()
        new_ucet_id = ucet_count + 1

        new_ucet = Ucet(new_ucet_id, ucet_jmeno=name, ucet_email=email, ucet_heslo=password, typ_uctu_id=3)

        session_maker.add(new_ucet)
        session_maker.commit()

        return redirect(url_for('views.prihlaseni'))

    return render_template('registrace.html', form=form)

#Odhlášení zákazníka
@views.route('/odhlaseni')
def odhlaseni():
    session.clear()
    return redirect(url_for('views.home'))

# získání objednávek do obou tabulek na stránce objednavky-k-potvrzeni
@views.route('/objednavky-k-potvrzeni')
def objednavky_k_potvrzeni():
    objednavky = session_maker.query(Objednavka).all()

    # ziskání ID objednávek, které jsou jako atributy u záznamů Rezervace, které mají rezervace_platnost nastavenou na False
    zrusene_rezervace_id = [rez.objednavka_id for rez in session_maker.query(Rezervace).filter_by(rezervace_platnost=False).all()]
    print(f"Tohle jsou zrusene rezervace: {zrusene_rezervace_id}")

    return render_template('objednavky-k-potvrzeni.html', objednavky=objednavky, zrusene_rezervace=zrusene_rezervace_id)

# získání seznamu všech pracovníků (techniku)
@views.route('/get-pracovnici')
def get_pracovnici():
    ucet_records = session_maker.query(Ucet).filter(Ucet.typ_uctu_id == 2).all()
    return jsonify([{ 'ucet_id': ucet.ucet_id, 'ucet_jmeno': ucet.ucet_jmeno } for ucet in ucet_records])


# vytvoření nového záznamu do tabulky Rezervace po přiřazení pracovníka dispečerem
@views.route('/vytvorit_rezervaci', methods=['POST'])
def vytvorit_rezervaci():
    data = request.json
    objednavka_id = data['objednavka_id']
    ucet_id = data['ucet_ids'][0]  # Assuming you're only selecting one Ucet

    # Create a new Rezervace instance
    new_rezervace = Rezervace(
        rezervace_id=None,
        rezervace_platnost=True,
        objednavka_id=objednavka_id,
        ucet_id=ucet_id  # Update this field name in your Rezervace model
    )

    objednavka = session_maker.query(Objednavka).filter_by(objednavka_id=objednavka_id).first()
    if objednavka:
        objednavka.objednavka_zpracovana = True
        session_maker.commit()

    # Add new record to the database
    session_maker.add(new_rezervace)
    session_maker.commit()

    return jsonify({'message': 'Rezervace created successfully'})


# Vypisování potvrzených rezervací na stránce profil.html
@views.route('/profil')
def profil():
    user_id = session.get('ucet_id')

    # pokud je uživatel přihlášen
    if user_id is not None:
        # Filtrování objednávek pouze pro přihlášeného zákazníka
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

        # Výpočet ceny
        # zpracovane_zaznamy = []
        # for zaznam in rezervace_zaznamy:
        #     hours = (zaznam[2] - zaznam[1]).total_seconds() / 3600
        #     cena = int(zaznam[4] * hours + zaznam[6] * hours)
        #     zpracovany_zaznam = tuple(zaznam) + (cena,)
        #     zpracovane_zaznamy.append(zpracovany_zaznam)

        zpracovane_zaznamy = []
        for zaznam in rezervace_zaznamy:
            hours = (zaznam[2] - zaznam[1]).total_seconds() / 3600
            fixed_cost = 150  # Fixed cost replacing Pracovnik cost
            cena = int(zaznam[4] * hours + fixed_cost * hours)
            zpracovany_zaznam = tuple(zaznam) + (cena,)
            zpracovane_zaznamy.append(zpracovany_zaznam)

        print(f"Tohle jsou rezervace_records {zpracovane_zaznamy}")
        return render_template('profil.html', rezervace_records=zpracovane_zaznamy)

    return redirect(url_for('views.prihlaseni'))

# Po kliknuti na button v profil.html se u vybrane rezervace nastavi atribut rezervace_platnost na False
# Provádí Zákazník
@views.route('/zrusit_rezervaci', methods=['POST'])
def zrusit_rezervaci():
    rezervace_id = request.form.get('rezervace_id')

    rezervace_to_cancel = session_maker.query(Rezervace).filter_by(rezervace_id=rezervace_id).first()
    if rezervace_to_cancel:
        # Po stisknuti tlačítka se rezervace oznaci jako False
        rezervace_to_cancel.rezervace_platnost = False
        session_maker.commit()

    return redirect(url_for('views.profil'))

# Po kliknutí na button Zrušit objednávku se objednávka i rezervace zruší
# Provádí Dispečer
@views.route('/zrusit_objednavku', methods=['POST'])
def zrusit_objednavku():
    objednavka_id = request.form.get('objednavka_id')

    # Vymaže Rezervaci, která má v sobě ID objednávky
    rezervace_to_delete = session_maker.query(Rezervace).filter_by(objednavka_id=objednavka_id).first()
    if rezervace_to_delete:
        session_maker.delete(rezervace_to_delete)

    # Vymaže objednávku s ID
    objednavka_to_delete = session_maker.query(Objednavka).filter_by(objednavka_id=objednavka_id).first()
    if objednavka_to_delete:
        session_maker.delete(objednavka_to_delete)

    session_maker.commit()

    return redirect(url_for('views.objednavky_k_potvrzeni'))

@views.route('/moje-zakazky')
def moje_zakazky():
    user_id = session.get('ucet_id')

    # Fetch Rezervace records for the logged-in user
    rezervace_zaznamy = session_maker.query(
        Rezervace.rezervace_id,
        Objednavka.objednavka_datum_od,
        Objednavka.objednavka_datum_do,
        Stroj.stroj_nazev
    ).join(Objednavka, Rezervace.objednavka_id == Objednavka.objednavka_id) \
     .join(Stroj, Objednavka.stroj_id == Stroj.stroj_id) \
     .filter(Rezervace.ucet_id == user_id).all()

    return render_template('moje-zakazky.html', rezervace_records=rezervace_zaznamy)

