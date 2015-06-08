#!/usr/bin/env python
# encoding: utf-8

from werkzeug.routing import Rule

urlpatterns = {
    Rule('/', endpoint='timeline'),
    Rule('/public', endpoint='public_timeline'),
    Rule('/<username>', endpoint='user_timeline'),
    Rule('/<username>/follow', endpoint='follow_user'),
    Rule('/<username>/unfollow', endpoint='unfollow_user'),
    Rule('/add_message', endpoint='add_message', methods=['POST']),
    Rule('/login', endpoint='login', methods=['GET', 'POST']),
    Rule('/register', endpoint='register', methods=['GET', 'POST']),
    Rule('/logout', endpoint='logout'),
}

