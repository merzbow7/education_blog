import base64
from datetime import datetime
from pathlib import Path

from flask import render_template, redirect, url_for, abort, request, flash, jsonify, g, session
from flask_security import current_user, auth_required
from flask_babel import _, get_locale, gettext, get_translations

from app import app, db, babel
from app.forms import AddNewPostForm, AddCommentForm, ProfileForm
from app.models import Post, Comment, User
from app.utils import add_to_db, get_post_hash


@app.route('/language/<language>')
def set_language(language=None):
    session["lang"] = language
    return redirect(request.args["next"])


@app.before_request
def before_request():
    session["lang"] = str(get_locale())
    if current_user.is_authenticated:
        current_user.last_login_at = datetime.utcnow()
        db.session.commit()


@app.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc())
    c_page = request.args.get('page', 1, type=int)
    page = posts.paginate(c_page, app.config["POSTS_PER_PAGE"], False)
    return render_template("index.html", page=page)


@app.route("/blog")
@auth_required('token', 'session')
def blog():
    posts = Post.query.filter_by(user_id=current_user.id).order_by(Post.created_at.desc())
    c_page = request.args.get('page', 1, type=int)
    page = posts.paginate(c_page, app.config["POSTS_PER_PAGE"], False)
    return render_template("index.html", page=page)


@app.route("/feed")
@auth_required('token', 'session')
def feed():
    posts = current_user.followed_posts()
    c_page = request.args.get('page', 1, type=int)
    page = posts.paginate(c_page, app.config["POSTS_PER_PAGE"], False)
    return render_template("index.html", page=page)


@app.route("/profile", methods=["POST", "GET"])
@auth_required('token', 'session')
def private_profile():
    profile_form = ProfileForm(obj=current_user)
    if profile_form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        filename = profile_form.file.data
        username = profile_form.username.data
        about = profile_form.about.data
        if filename:
            file = request.files['file'].read()
            user.user_avatar = file
        if username:
            user.username = username
        if about:
            user.about = about
        try:
            db.session.commit()
            flash(gettext('Changes saved.'), "success")
            return redirect(url_for("private_profile"))
        except Exception as err:
            db.session.rollback()
            flash(gettext('Error'), "danger")
            app.logger.error(f"sql error: {err}")
    return render_template("edit_profile.html", form=profile_form)


@app.route("/profile/<username>")
@auth_required('token', 'session')
def profile(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj:
        if user_obj.user_avatar:
            avatar = base64.b64encode(user_obj.user_avatar).decode('ascii')
        else:
            avatar = False
        tab = request.args.get("tab", "Posts")

        c_page = request.args.get('page', 1, type=int)
        page = eval(tab[:-1]).query.filter_by(user_id=user_obj.id).paginate(c_page, 8, False)
        params = {"username": username, "tab": tab}
        return render_template("public_profile.html", user=user_obj, avatar=avatar, tab=tab,
                               page=page, params=params)
    else:
        abort(404)


@app.route("/post/<post_hash>", methods=["POST", "GET"])
def post(post_hash):
    getting_post = Post.query.filter_by(hash_name=post_hash)
    comment_form = AddCommentForm()
    if getting_post.count():
        if comment_form.validate_on_submit():
            comment = Comment(body=comment_form.comment.data, post_id=getting_post.first().id,
                              user_id=current_user.id)
            add_to_db(comment)
            return redirect(url_for("post", post_hash=post_hash))
        c_page = request.args.get('page', 1, type=int)
        page = getting_post.first().comments.paginate(c_page, app.config["COMMENTS_PER_PAGE"], False)
        params = {"post_hash": post_hash}
        return render_template("post.html", post=getting_post.first(),
                               add_comment_form=comment_form, page=page, params=params)
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


@app.route("/subscriptions")
@auth_required('token', 'session')
def subscriptions():
    return render_template("subscriptions.html")


@app.route("/subscribe")
@auth_required('token', 'session')
def subscribe():
    subscriber = User.query.get(current_user.id)
    recipient = User.query.filter_by(username=request.args["recipient"]).first()
    action = request.args["action"]
    try:
        if action == "append":
            subscriber.follow(recipient)
        elif action == "remove":
            subscriber.unfollow(recipient)
        db.session.commit()
        return jsonify({"good": "ok"})
    except Exception as err:
        app.logger.error(f"sql error: {err}")
        return jsonify({"error": "Error"})


@app.route("/links")
def links():
    links = (
        "https://flask-migrate.readthedocs.io/en/latest/",
        "https://flask-security-too.readthedocs.io/en/stable/index.html")
    return render_template("links.html", links=links)


# error section

@app.errorhandler(404)
def not_found_error(error):
    app.logger.warning(f"cant resolve url: {request.url}")
    return render_template('error.html', error=404), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"internal error: {error}")
    return render_template('error.html', error=500), 500
