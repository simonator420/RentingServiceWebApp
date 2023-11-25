from flask import *
from forms import *
from database.database import *
from markupsafe import Markup
from werkzeug.utils import secure_filename
from datetime import datetime


views = Blueprint(__name__, 'views')
click=0

#Hlavní stránka při prvním načtení
@views.route('/')
def homer():
    return render_template('index.html')

#Hlavní stránka
@views.route('/index.html')
def home():
    return render_template('index.html')

#O nás
@views.route('/o-nas')
def onas():
    return render_template('index.html', target_section='o-nas')

#Výpis strojů
@views.route('/nabidka-stroju', methods=['GET', 'POST'])
def nabidka_stroju():
    if request.method == 'POST':
        # Check if this is a form submission for creating an Objednavka
        if 'stroj_id' in request.form:
            stroj_id = request.form['stroj_id']
            datum_od_str = request.form['datum_od']
            datum_do_str = request.form['datum_do']

            # Convert string dates to Python date objects
            datum_od = datetime.strptime(datum_od_str, '%Y-%m-%d').date()
            datum_do = datetime.strptime(datum_do_str, '%Y-%m-%d').date()

            new_objednavka = Objednavka(
                objednavka_id = None,  # Assuming autoincrement is enabled
                objednavka_datum_od = datum_od,
                objednavka_datum_do = datum_do,
                stroj_id = stroj_id
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

@views.route('/objednavky-k-potvrzeni')
def objednavky_k_potvrzeni():
    objednavky = session_maker.query(Objednavka).all()  # Query all Objednavka records

    return render_template('objednavky-k-potvrzeni.html', objednavky=objednavky)

@views.route('/get-pracovnici')
def get_pracovnici():
    pracovnici = session_maker.query(Pracovnik).all()
    return jsonify([{ 'pracovnik_id': pracovnik.pracovnik_id, 'pracovnik_jmeno': pracovnik.pracovnik_jmeno } for pracovnik in pracovnici])
