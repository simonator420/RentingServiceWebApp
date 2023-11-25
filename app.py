from flask import Flask, session
from views import views
from database.database import Base, engine, session_maker, Typ_stroje

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")
app.config['SECRET_KEY'] = '123'

# Nastavení user_name pro umístění v záhlaví ve všech stránkách
@app.context_processor
def set_user_name():
    return {'user_name': session.get('user_name')}

@app.context_processor
def set_typ_stroje_values():
    typ_stroje_values = session_maker.query(Typ_stroje.typ_stroje_nazev).distinct().all()
    
    # Extract the values from the query result
    typ_stroje_values = [value[0] for value in typ_stroje_values]
    print(f"Tohle jsou stroje values{typ_stroje_values}")

    return {'typ_stroje_values': typ_stroje_values}

@app.context_processor
def set_typ_uctu_id():
    return {'typ_uctu': session.get('typ_uctu_id')}

Base.metadata.create_all(engine)



if __name__ == '__main__':
    app.run(debug=True)