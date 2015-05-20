#!/usr/bin/env python
# encoding: utf-8

from app.db import db
from app.db.orm.user import User


class UserModel(object):
    def get_id(self, username):
        user = User.query.filter(User.username == username).first()

        return user.user_id if user else None

    def find(self, **kwargs):
        query = User.query

        for attr, value in kwargs.iteritems():
            query = query.filter(getattr(User, attr) == value)

        return query.first()

    def add(self, username, password, email):
        data = {
            'username': username,
            'pw_hash': password,
            'email': email
        }

        user = User(**data)

        db.session.add(user)
        db.session.commit()
