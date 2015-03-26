# -*- coding: utf-8 -*-

import os
from app import app
from app import init_db

if __name__ == '__main__':
    init_db()  # create database schema
    port = int(os.environ.get("PORT", 8080))
    app.run('0.0.0.0', port=port)
