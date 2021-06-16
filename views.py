import base64
from datetime import datetime

from flask import render_template, redirect, url_for, abort, request
from flask_security import current_user, auth_required

from app import app, db
from forms import AddNewPostForm, AddCommentForm, ProfileForm
from models import Post, Comment, User
from utils import add_to_db, get_post_hash


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login_at = datetime.utcnow()
        db.session.commit()


@app.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc())
    return render_template("index.html", posts=posts)


@app.route("/blog")
@auth_required('token', 'session')
def blog():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc())
    return render_template("index.html", posts=posts)


@app.route("/profile", methods=["POST", "GET"])
@auth_required('token', 'session')
def private_profile():
    profile_form = ProfileForm()
    if profile_form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        file = request.files['file'].read()
        user.user_avatar = file
        user.username = profile_form.username.data
        try:
            db.session.commit()
        except Exception as err:
            print(f"SQL error: {err}")
    return render_template("profile.html", form=profile_form)


@app.route("/user/<username>")
def user(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj:
        if user_obj.user_avatar:
            avatar = base64.b64encode(user_obj.user_avatar).decode('ascii')
        else:
            avatar = False
        return render_template("user.html", user=user_obj, avatar=avatar)
    else:
        abort(404)


@app.route("/user/<username>/avatar")
def user_avatar(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj.user_avatar:
        avatar = base64.b64encode(user_obj.user_avatar).decode('ascii')
    else:
        avatar = False
    result = "data:;base64," + avatar
    html = f'<img class="float-start me-2" src="data:;base64,{avatar}"/>'
    return html


@app.route("/post/<post_hash>", methods=["POST", "GET"])
def post(post_hash):
    getting_post = Post.query.filter_by(hash_name=post_hash)
    comment_form = AddCommentForm()
    if getting_post.count():
        if comment_form.validate_on_submit():
            comment = Comment(body=comment_form.comment.data, post_id=getting_post.first().id,
                              user_id=current_user.id)
            add_to_db(comment)
        comment_form.comment.data = ""
        return render_template("post.html", post=getting_post.first(), add_comment_form=comment_form)
    else:
        return abort(404)


@app.route("/newpost", methods=["POST", "GET"])
@auth_required('token', 'session')
def new_post():
    post_form = AddNewPostForm()
    if post_form.validate_on_submit():
        post = Post(title=post_form.title.data, body=post_form.post.data,
                    user_id=current_user.id, hash_name=get_post_hash())
        add_to_db(post)
        return redirect(url_for("blog"))
    return render_template("new_post.html", add_post_form=post_form)


@app.route("/feed")
@auth_required('token', 'session')
def feed():
    return render_template("index.html")


@app.route("/links")
def links():
    links = (
        "https://flask-migrate.readthedocs.io/en/latest/",
        "https://flask-security-too.readthedocs.io/en/stable/index.html")
    return render_template("links.html", links=links)


# error section

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error=404), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=500), 500


# Context

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, "Comment": Comment}
