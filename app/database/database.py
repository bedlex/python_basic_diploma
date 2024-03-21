""" Module to handle database structure. """
from app import metadata
from sqlalchemy import Table, Column
from sqlalchemy import String, Integer, TIMESTAMP, ForeignKey, TEXT


users = Table('users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String(32)),
              Column('first_name', String(64)),
              Column('last_name', String(64)),
              Column('timestamp', TIMESTAMP))

bookmarks = Table('bookmarks', metadata,
                  Column('id', Integer, primary_key=True, autoincrement=True),
                  Column('symbol', String(50)),
                  Column('user_id', ForeignKey('users.id')),
                  Column('timestamp', TIMESTAMP))

history = Table('history', metadata,
                Column('id', Integer, primary_key=True, autoincrement=True),
                Column('request', String(250)),
                Column('respond', TEXT),
                Column('user_id', ForeignKey('users.id')),
                Column('timestamp', TIMESTAMP)
                )