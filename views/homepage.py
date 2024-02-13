from flask import Blueprint, render_template, redirect, url_for, request

from database.database import session_maker, Typ_stroje, Stroj
from forms import ObjednavkaForm, SearchForm

homepage = Blueprint('homepage', __name__)

@homepage.route('/', methods=['GET', 'POST'], endpoint='home')
def home():
    form = ObjednavkaForm()
    search_form = SearchForm()
    results = []

    # ziskani hodnot typ stroje z databaze
    typ_stroje_values = session_maker.query(Typ_stroje.typ_stroje_nazev).distinct().all()
    # dynamicke nastaveni hodnot typu stroje do atributu dropboxu - choices
    search_form.type.choices = [(value.typ_stroje_nazev, value.typ_stroje_nazev) for value in typ_stroje_values]

    if request.method == 'POST' and search_form.validate_on_submit():

        typ = form.type.data
        datum_od = form.date_from.data
        datum_do = form.date_to.data

        pass

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

    # Vrátí šablonu index.jinja s předanými daty
    return render_template('homepage/index.jinja', form=form, search_form=search_form, results=results)

@homepage.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    if request.method == 'POST' and form.validate_on_submit():

        typ = form.type.data
        datum_od = form.date_from.data
        datum_do = form.date_to.data

    return redirect(url_for('order.nabidka_stroju'))
