from . import db
import string
import random

def generate_short_id(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(512))
    short_id = db.Column(db.String(6), unique=True, nullable=False, default=generate_short_id)
