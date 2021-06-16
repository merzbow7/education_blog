from app import db, fsqla
from hashlib import md5
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Text, LargeBinary
from datetime import datetime
from random import choice
from string import ascii_lowercase


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(db.Model, fsqla.FsUserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    password = Column(String(255), nullable=False)
    active = Column(Boolean())
    last_login_at = Column(DateTime())
    user_avatar = Column(LargeBinary())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan", lazy='dynamic')
    comments = db.relationship('Comment', backref='user', cascade="all, delete-orphan", lazy='dynamic')
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))

    def avatar(self, size=32):
        digest = md5(''.join([choice(ascii_lowercase) for _ in range(12)]).encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Post(db.Model):
    __tablename__ = 'post'
    id = Column(Integer(), primary_key=True)
    hash_name = Column(String(25), unique=True, nullable=False)
    title = Column(String(50))
    body = Column(Text())
    user_id = Column(Integer(), ForeignKey('user.id'))
    created_at = Column(DateTime(), default=datetime.now)
    comments = db.relationship('Comment', cascade="all, delete-orphan", backref='post', lazy='dynamic')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer(), primary_key=True)
    post_id = Column(Integer(), ForeignKey('post.id'))
    user_id = Column(Integer(), ForeignKey('user.id'))
    body = Column(String(255))
    created_at = Column(DateTime(), default=datetime.now)
