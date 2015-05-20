# -*- coding: utf-8 -*-

from app.db import db


class Follower(db.Model):
    __tablename__ = 'follower'

    who_id = db.Column(db.Integer, primary_key=True)
    whom_id = db.Column(db.Integer, primary_key=True)
