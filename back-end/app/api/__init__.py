from flask import Blueprint

bp=Blueprint('api',__name__)

from app.api import detect
from app.api import remove_json
