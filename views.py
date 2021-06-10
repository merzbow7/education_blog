from flask import render_template, redirect, url_for
from app import app, db
from models import Post
from flask_security import current_user, url_for_security
from forms import AddNewPostForm
from datetime import datetime


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/blog")
def blog():
    posts = Post.query.order_by(Post.created_at.desc())
    return render_template("index.html", posts=posts)


@app.route("/office")
def office():
    if current_user.has_role('admin'):
        return redirect(url_for('admin.index'))
    return render_template("office.html")


@app.route("/newpost", methods=["POST", "GET"])
def new_post():
    post_form = AddNewPostForm()
    if post_form.validate_on_submit():
        print(post_form.title.data)
        post = Post(title=post_form.title.data, body=post_form.post.data, created_at=datetime.now())
        try:
            db.session.add(post)
            db.session.commit()
        except (Exception):
            print("Error")
            db.session.rollback()
        return redirect(url_for("blog"))
    return render_template("new_post.html", add_post_form=post_form)


@app.route("/feed")
def feed():
    return render_template("index.html")


@app.route("/links")
def links():
    links = (
        "https://flask-migrate.readthedocs.io/en/latest/",
        "https://flask-security-too.readthedocs.io/en/stable/index.html")
    return render_template("links.html", links=links)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=404), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=500), 500