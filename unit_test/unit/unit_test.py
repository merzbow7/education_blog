import unittest
from datetime import timedelta, datetime

from flask_security import hash_password, verify_password

from app import create_app, db
from app.models import User, Post
from settings import TestConfig


class UserModelCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = create_app(TestConfig)

    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='john1', email='john1@example.com', password=hash_password('cat'), fs_uniquifier="123")
        self.assertFalse(verify_password('dog', u.password))
        self.assertTrue(verify_password('cat', u.password))

    def test_avatar(self):
        u = User(username='john', email='john@example.com', password=hash_password('cat'), fs_uniquifier="123")
        self.assertEqual(u.avatar(128),
                         ('https://www.gravatar.com/avatar/e3cd90a297bdc1853ac7a4b05f238876?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com', password=hash_password('cat'), fs_uniquifier="123")
        u2 = User(username='susan', email='susan@example.com', password=hash_password('cat'), fs_uniquifier="321")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
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
        self.assertEqual(f1, [p2, p4])
        self.assertEqual(f2, [p3])
        self.assertEqual(f3, [p4])
        self.assertEqual(f4, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
