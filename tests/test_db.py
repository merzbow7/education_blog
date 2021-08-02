from datetime import datetime, timedelta

import pytest
from flask_security import hash_password, verify_password

from app.models import User, Post


@pytest.mark.shallow
def test_password_hashing(init_db):
    u = User(username='john1', email='john1@example.com', password=hash_password('cat'), fs_uniquifier="123")
    assert not verify_password('dog', u.password)
    assert verify_password('cat', u.password)


def test_avatar(init_db):
    u = User(username='john', email='john@example.com', password=hash_password('cat'), fs_uniquifier="123")
    assert u.avatar(128) == 'https://www.gravatar.com/avatar/e3cd90a297bdc1853ac7a4b05f238876?d=identicon&s=128'


def test_follow(init_db):
    db = init_db
    u1 = User(username='john', email='john@example.com', password=hash_password('cat'), fs_uniquifier="123")
    u2 = User(username='susan', email='susan@example.com', password=hash_password('cat'), fs_uniquifier="321")
    db.session.add(u1)
    db.session.add(u2)
    db.session.commit()
    assert u1.followed.all() == []
    assert u1.followers.all() == []

    u1.follow(u2)
    db.session.commit()
    assert u1.is_following(u2)
    assert u1.followed.count() == 1
    assert u1.followed.first().username == 'susan'
    assert u2.followers.count() == 1
    assert u2.followers.first().username == 'john'

    u1.unfollow(u2)
    db.session.commit()
    assert not u1.is_following(u2)
    assert u1.followed.count() == 0
    assert u2.followers.count() == 0


def test_follow_posts(init_db):
    db = init_db
    # create four users
    u1 = User(username='john', email='john@example.com', password=hash_password('cat'), fs_uniquifier="123")
    u2 = User(username='susan', email='susan@example.com', password=hash_password('cat'), fs_uniquifier="1234")
    u3 = User(username='mary', email='mary@example.com', password=hash_password('cat'), fs_uniquifier="12345")
    u4 = User(username='david', email='david@example.com', password=hash_password('cat'), fs_uniquifier="123456")
    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()

    # create four posts
    now = datetime.utcnow()
    p1 = Post(title="test1", hash_name="asda1", body="post from john", user_id=u1.id,
              created_at=now + timedelta(seconds=1))
    p2 = Post(title="test2", hash_name="asda2", body="post from susan", user_id=u2.id,
              created_at=now + timedelta(seconds=4))
    p3 = Post(title="test3", hash_name="asda3", body="post from mary", user_id=u3.id,
              created_at=now + timedelta(seconds=3))
    p4 = Post(title="test4", hash_name="asda4", body="post from david", user_id=u4.id,
              created_at=now + timedelta(seconds=2))
    db.session.add_all([p1, p2, p3, p4])
    db.session.commit()

    u1.follow(u2)  # john follows susan
    u1.follow(u4)  # john follows david
    u2.follow(u3)  # susan follows mary
    u3.follow(u4)  # mary follows david
    db.session.commit()

    # check the followed posts of each user
    f1 = u1.followed_posts().all()
    f2 = u2.followed_posts().all()
    f3 = u3.followed_posts().all()
    f4 = u4.followed_posts().all()
    assert f1 == [p2, p4]
    assert f2 == [p3]
    assert f3 == [p4]
    assert f4 == []
