from flask import Blueprint

api = Blueprint('api',__name__)

from . import verification_code, passport, profile, house,orders,pay