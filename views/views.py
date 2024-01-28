from flask import *
from forms.forms import *
from database.database import *
from werkzeug.security import check_password_hash
import datetime


views = Blueprint('views', __name__)
click=0




