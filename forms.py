from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from wtforms.widgets import *

#Struktura formuláře pro přihlášení zákazníka
class SingupForm(FlaskForm):
    name= StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up', validators=[DataRequired()])
    
#Registrace zákazníka
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email(message='Please enter a valid email')])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register', validators=[DataRequired()])

#Stroje k dispozici a jejich informace zadané technikem
class StrojForm(FlaskForm): 
    nazev = StringField('Název', validators=[DataRequired()])
    cena = FloatField('Cena', validators=[DataRequired()])
    typ =  StringField('Typ', validators=[DataRequired()])
    submit = SubmitField('Přidej Stroj')

#Formulář na vytvoření objednávky 
class ObjednavkaForm(FlaskForm):
    nazev = StringField('Název', validators=[DataRequired()])
    cena = FloatField('Cena', validators=[DataRequired()])
    typ =  StringField('Typ', validators=[DataRequired()])
    datum_od = DateField('Datum od', validators=[DataRequired()])
    datum_do= DateField('Datum do', validators=[DataRequired()])
    submit= SubmitField('Přidej Objednávku')

#Formulář na vytvoření Pracovnika 
class PracovnikForm(FlaskForm):
    jmeno= StringField('Jméno', validators=[DataRequired()])
    cena= FloatField('Cena', validators=[DataRequired()])
    submit= SubmitField('Přidej Pracovnika')

class SelectValuesForm(FlaskForm):
    machine_type = StringField('Typ stroje', validators=[DataRequired()])
    datum_od = DateField('Od kdy', validators=[DataRequired()])
    datum_do = DateField('Do kdy', validators=[DataRequired()])
    submit= SubmitField('OK')

