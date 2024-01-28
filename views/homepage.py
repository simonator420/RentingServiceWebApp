from flask import Blueprint, render_template

from database.database import session_maker, Typ_stroje, Stroj
from forms.forms import ObjednavkaForm

homepage = Blueprint('homepage', __name__)

@homepage.route('/', methods=['GET', 'POST'], endpoint='home')
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

    # Vrátí šablonu index.jinja s předanými daty
    return render_template('homepage/index.jinja', form=form, results=results)
