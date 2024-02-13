from flask import *
from forms import *
from database.database import *
import datetime

order = Blueprint('order', __name__)

#Výpis strojů
@order.route('/nabidka-stroju', methods=['GET', 'POST'])
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

    # Vrátí šablonu nabidka-stroju.jinja s daty o strojích
    return render_template('order/nabidka-stroju.jinja', stroje=stroje)

@order.route('/objednavky-k-potvrzeni')
def objednavky_k_potvrzeni():
    # Dotaz do databáze pro získání všech objednávek
    objednavky = session_maker.query(Objednavka).all()

    # Získání ID objednávek s neplatnou rezervací
    zrusene_rezervace_id = [rez.objednavka_id for rez in session_maker.query(Rezervace).filter_by(rezervace_platnost=False).all()]

    # Vrátí šablonu objednavky-k-potvrzeni.jinja s daty o objednávkách
    return render_template('order/objednavky-k-potvrzeni.jinja', objednavky=objednavky, zrusene_rezervace=zrusene_rezervace_id)

# Vytvoření nového záznamu do tabulky Rezervace po přiřazení pracovníka dispečerem
@order.route('/vytvorit_rezervaci', methods=['POST'])
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

# Zrušení rezervace uživatelem
@order.route('/zrusit_rezervaci', methods=['POST'])
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
    return redirect(url_for('profile.profil'))

# Zrušení objednávky dispečerem
@order.route('/zrusit_objednavku', methods=['POST'])
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
    return redirect(url_for('order.objednavky_k_potvrzeni'))

# Zobrazení zakázek přihlášeného uživatele
@order.route('/moje-zakazky')
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

    # Vrátí šablonu moje-zakazky.jinja s daty o rezervacích
    return render_template('order/moje-zakazky.jinja', rezervace_records=rezervace_zaznamy)