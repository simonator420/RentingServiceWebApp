from flask import Flask, session
from views.profile import profile
from views.homepage import homepage
from views.order import order
from database.database import Base, engine, session_maker, Typ_stroje

app = Flask(__name__)
app.register_blueprint(homepage, url_prefix="/")
app.register_blueprint(profile, url_prefix="/profile")
app.register_blueprint(order, url_prefix="/order")

app.config['SECRET_KEY'] = '123'

# Kontextový procesor pro nastavení jména uživatele v záhlaví všech stránek
@app.context_processor
def set_user_name():
    # Vrací user_name s hodnotou získanou ze session
    return {'user_name': session.get('user_name')}

# Kontextový procesor pro získání typů strojů pro vyplnění comboboxu
@app.context_processor
def set_typ_stroje_values():
    typ_stroje_values = session_maker.query(Typ_stroje.typ_stroje_nazev).distinct().all()
    # Převedení výsledků dotazu na seznam
    typ_stroje_values = [value[0] for value in typ_stroje_values]
    # Vrací typ_stroje_values se seznamem názvů typů strojů
    return {'typ_stroje_values': typ_stroje_values}

# Kontextový procesor pro nastavení typu uživatelského účtu
@app.context_processor
def set_typ_uctu_id():
    # Vrací typ_uctu s hodnotou typu uživatelského účtu ze session
    return {'typ_uctu': session.get('typ_uctu_id')}

# Kontextový procesor pro nastavení ID uživatele
@app.context_processor
def set_user_id():
    # Vrací ucet_id s hodnotou ID uživatele ze session
    return {'ucet_id': session.get('ucet_id')}

Base.metadata.create_all(engine)


if __name__ == '__main__':
    app.run(debug=True)