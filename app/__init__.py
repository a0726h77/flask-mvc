# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
app = Flask('app')
app.debug = True

# import controllers
from app.controllers import *

# import model
from models.models import db


# Creates the database tables.
def init_db():
    from sqlite3 import dbapi2 as sqlite3
    app.config.from_pyfile('config/database.cfg')
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


#### initial logger ####
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_PATH = '/'.join((os.path.dirname(os.path.realpath(__file__)), 'log'))
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

handler = RotatingFileHandler(LOG_PATH + '/debug.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
#### initial logger ####


#### initial sesion ####
from datetime import timedelta
app.config['SECRET_KEY'] = 'random'
app.permanent_session_lifetime = timedelta(seconds=60*60*10)  # session expire time
#### initial sesion ####


#### initial database ####
app.config.from_pyfile('config/database.cfg')
db.init_app(app)
#### initial database ####


#### router ####
from url import urlpatterns

for rule in urlpatterns:
    app.url_map.add(rule)
#### router ####
