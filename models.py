from app import db, fsqla
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Boolean, DateTime, Column, Integer, String, ForeignKey, Text


# class RolesUsers(db.Model):
#     id = Column(Integer(), primary_key=True)
#     user_id = Column('user_id', Integer(), ForeignKey('user.id'))
#     role_id = Column('role_id', Integer(), ForeignKey('role.id'))


class Role(db.Model, fsqla.FsRoleMixin):
    __tablename__ = 'role'
    id = Column(Integer(), primary_key=True)
    name = Column(String(80), unique=True)
    description = Column(String(255))


class User(db.Model, fsqla.FsUserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    username = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    active = Column(Boolean())
    fs_uniquifier = Column(String(255), unique=True, nullable=False)
    confirmed_at = Column(DateTime())
    roles = relationship('Role', secondary='roles_users',
                         backref=backref('users', lazy='dynamic'))


class Post(db.Model):
    __tablename__ = 'post'
    id = Column(Integer(), primary_key=True)
    title = Column(String(50))
    body = Column(Text(), unique=True)
    created_at = Column(DateTime())


class Comment(db.Model):
    __tablename__ = 'comment'
    id = Column(Integer(), primary_key=True)
    body = Column(String(255), unique=True)
    created_at = Column(DateTime())
