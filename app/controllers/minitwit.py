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
from app.models.message import MessageModel
from app.models.follower import FollowerModel

user_model = UserModel()
message_model = MessageModel()
follower_model = FollowerModel()

# configuration
PER_PAGE = 30


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


@app.endpoint('timeline')
def timeline():
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    if not g.user:
        return redirect(url_for('public_timeline'))

    results = message_model.getUserFollowerTimeline(session['user_id'], PER_PAGE)

    return render_template('twit/timeline.html', results=results)


@app.endpoint('public_timeline')
def public_timeline():
    """Displays the latest messages of all users."""
    results = message_model.getAll(PER_PAGE)

    return render_template('twit/timeline.html', results=results)


@app.endpoint('user_timeline')
def user_timeline(username):
    """Display's a users tweets."""
    profile_user = user_model.find(**{'username': username})
    if profile_user is None:
        abort(404)

    followed = False
    if g.user:
        followed = follower_model.followed(session['user_id'], profile_user.user_id)

    results = message_model.getUserTimeline(profile_user.user_id, limit=PER_PAGE)

    return render_template('twit/timeline.html', results=results, followed=followed, profile_user=profile_user)


@app.endpoint('follow_user')
def follow_user(username):
    """Adds the current user as follower of the given user."""
    if not g.user:
        abort(401)
    whom_id = user_model.get_id(username)
    if whom_id is None:
        abort(404)

    follower_model.add(session['user_id'], whom_id)

    flash('You are now following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))


@app.endpoint('unfollow_user')
def unfollow_user(username):
    """Removes the current user as follower of the given user."""
    if not g.user:
        abort(401)
    whom_id = user_model.get_id(username)
    if whom_id is None:
        abort(404)

    follower_model.delete(session['user_id'], whom_id)

    flash('You are no longer following "%s"' % username)
    return redirect(url_for('user_timeline', username=username))


@app.endpoint('add_message')
def add_message():
    """Registers a new message for the user."""
    if 'user_id' not in session:
        abort(401)
    if request.form['text']:
        message_model.add(session['user_id'], request.form['text'])

        flash('Your message was recorded')
    return redirect(url_for('timeline'))


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = user_model.find(**{'user_id': session['user_id']})


# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url
