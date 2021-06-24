from app import db
from flask_security.models import fsqla_v2 as fsqla
from hashlib import md5
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Text, LargeBinary
from datetime import datetime

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class Role(db.Model, fsqla.FsRoleMixin):
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(db.Model, fsqla.FsUserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(25), unique=True)
    password = Column(String(255), nullable=False)
    about = Column(String(255))
    active = Column(Boolean())
    last_login_at = Column(DateTime())
    user_avatar = Column(LargeBinary())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan", lazy='dynamic')
    comments = db.relationship('Comment', backref='user', cascade="all, delete-orphan", lazy='dynamic')
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))
    followed = db.relationship('User', secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def set_password(self):
        pass

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(
            Post.created_at.desc())

    @classmethod
    def is_name_exist(cls, name):
        if cls.query.filter_by(username=name).count():
            return True

    def avatar(self, size=32):
        digest = md5(str(self.email + self.username).encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'


class Post(db.Model):
    id = Column(Integer(), primary_key=True)
    hash_name = Column(String(25), unique=True, nullable=False)
    title = Column(String(50))
    body = Column(Text())
    user_id = Column(Integer(), ForeignKey('user.id'))
    created_at = Column(DateTime(), default=datetime.utcnow)
    comments = db.relationship('Comment', cascade="all, delete-orphan", backref='post', lazy='dynamic')


class Comment(db.Model):
    id = Column(Integer(), primary_key=True)
    post_id = Column(Integer(), ForeignKey('post.id'))
    user_id = Column(Integer(), ForeignKey('user.id'))
    body = Column(String(255))
    created_at = Column(DateTime(), default=datetime.utcnow)
