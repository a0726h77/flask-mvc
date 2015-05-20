#!/usr/bin/env python
# encoding: utf-8

from app.db import db
from app.db.orm.follower import Follower


class FollowerModel(object):
    def followed(self, who_id, whom_id):
        followed = False

        follower = Follower.query.filter(Follower.who_id == who_id, Follower.whom_id == whom_id).first()

        if follower:
            followed = True

        return followed

    def add(self, who_id, whom_id):
        data = {
            'who_id': who_id,
            'whom_id': whom_id
        }

        follower = Follower(**data)

        db.session.add(follower)
        db.session.commit()

    def delete(self, who_id, whom_id):
        Follower.query.filter(Follower.who_id == who_id).filter(Follower.whom_id == whom_id).delete()
        db.session.commit()
