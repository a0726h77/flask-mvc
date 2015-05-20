# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~

    A microblogging application written with Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

from app import app
import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash

from app.models.user import UserModel

user_model = UserModel()

# configuration
# PER_PAGE = 30

# create our little application :)
# app = Flask(__name__)
# app.config.from_object(__name__)
# app.config.from_envvar('MINITWIT_SETTINGS', silent=True)


# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     top = _app_ctx_stack.top
#     if not hasattr(top, 'sqlite_db'):
#         top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
#         top.sqlite_db.row_factory = sqlite3.Row
#     return top.sqlite_db


# @app.teardown_appcontext
# def close_database(exception):
#     """Closes the database again at the end of the request."""
#     top = _app_ctx_stack.top
#     if hasattr(top, 'sqlite_db'):
#         top.sqlite_db.close()


# def init_db():
#     """Creates the database tables."""
#     with app.app_context():
#         db = get_db()
#         with app.open_resource('schema.sql', mode='r') as f:
#             db.cursor().executescript(f.read())
#         db.commit()


# def query_db(query, args=(), one=False):
#     """Queries the database and returns a list of dictionaries."""
#     cur = get_db().execute(query, args)
#     rv = cur.fetchall()
#     return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = user_model.find(**{'user_id': session['user_id']})


@app.endpoint('login')
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        user = user_model.find(**{'username': request.form['username']})
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user.pw_hash,
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user.user_id
            return redirect(url_for('timeline'))
    return render_template('rbac/login.html', error=error)


@app.endpoint('register')
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                 '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif user_model.get_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            data = dict([[k, v] for k, v in request.form.items()])

            data['pw_hash'] = generate_password_hash(data['password'])

            del data['password']
            del data['password2']

            user_model.add(data['username'], data['pw_hash'], data['email'])

            flash('You were successfully registered and can login now')
            return redirect(url_for('login'))
    return render_template('rbac/register.html', error=error)


@app.endpoint('logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('public_timeline'))
