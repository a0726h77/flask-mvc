#!/usr/bin/env python
# encoding: utf-8

import time

from app.db import db
from app.db.orm.user import User
from app.db.orm.message import Message
from app.db.orm.follower import Follower


class MessageModel(object):
    def get_id(self, username):
        user = User.query.filter(User.username == username).first()

        return user.user_id if user else None

    def find(self, **kwargs):
        query = User.query

        for attr, value in kwargs.iteritems():
            query = query.filter(getattr(User, attr) == value)

        return query.first()

    def findAll(self, limit=None, **kwargs):
        query = db.session.query(Message, User).filter(Message.author_id == User.user_id)

        for attr, value in kwargs.iteritems():
            query = query.filter(getattr(User, attr) == value)

        query = query.order_by(Message.pub_date.desc()).limit(limit)

        return query.all()

    def getAll(self, limit=None):
        results = db.session.query(Message, User).filter(Message.author_id == User.user_id).order_by(Message.pub_date.desc()).limit(limit).all()

        return results

    def getUserTimeline(self, user_id, limit=None):
        results = db.session.query(Message, User).filter(Message.author_id == User.user_id).filter(User.user_id == user_id).order_by(Message.pub_date.desc()).limit(limit).all()

        return results

    def getUserFollowerTimeline(self, user_id, limit=None):
        results = db.session.query(Message, User).filter(Message.author_id == User.user_id).filter(db.or_(User.user_id == user_id, User.user_id.in_(Follower.query.with_entities(Follower.whom_id).filter(Follower.who_id == user_id)))).order_by(Message.pub_date.desc()).limit(limit).all()

        return results

    def add(self, user_id, text):
        data = {
            'author_id': user_id,
            'text': text,
            'pub_date': int(time.time())
        }

        message = Message(**data)
        db.session.add(message)
        db.session.commit()

        return message.message_id
