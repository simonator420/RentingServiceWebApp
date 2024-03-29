from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *

class SearchForm(FlaskForm):
    type = SelectField('Typ stroje: ', choices=[], validators=[DataRequired()])
    date_from = DateField('Datum od: ', validators=[DataRequired()])
    date_to = DateField('Datum do: ', validators=[DataRequired()])
    submit = SubmitField('OK', validators=[DataRequired()])


# Struktura formuláře pro přihlášení zákazníka
class SingupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up', validators=[DataRequired()])


# Registrace zákazníka
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register', validators=[DataRequired()])


# Stroje k dispozici a jejich informace zadané technikem
class StrojForm(FlaskForm):
    nazev = StringField('Název', validators=[DataRequired()])
    cena = FloatField('Cena', validators=[DataRequired()])
    typ = StringField('Typ', validators=[DataRequired()])
    submit = SubmitField('Přidej Stroj')


# Formulář na vytvoření objednávky
class ObjednavkaForm(FlaskForm):
    nazev = StringField('Název', validators=[DataRequired()])
    cena = FloatField('Cena', validators=[DataRequired()])
    typ = StringField('Typ', validators=[DataRequired()])
    datum_od = DateField('Datum od', validators=[DataRequired()])
    datum_do = DateField('Datum do', validators=[DataRequired()])
    submit = SubmitField('Přidej Objednávku')


# Formulář na vytvoření Pracovnika
class PracovnikForm(FlaskForm):
    jmeno = StringField('Jméno', validators=[DataRequired()])
    cena = FloatField('Cena', validators=[DataRequired()])
    submit = SubmitField('Přidej Pracovnika')

