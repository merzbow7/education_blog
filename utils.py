from app import db
from string import ascii_lowercase
from random import choice
from models import Post
import base64


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic


def make_random_hash(hash_len):
    return "".join([choice(ascii_lowercase) for _ in range(hash_len)])


def get_post_hash(hash_len=None):
    hash_len = 10 if not hash_len else hash_len
    post_hash = make_random_hash(hash_len)
    while Post.query.filter_by(hash_name=post_hash).count():
        post_hash = make_random_hash(hash_len)
    print(f"post_hash {post_hash}")
    return post_hash


def add_to_db(item):
    try:
        db.session.add(item)
        db.session.commit()
        return True
    except Exception as err:
        print(f"Error {err}")
        db.session.rollback()
        return False
