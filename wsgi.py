from app import create_app, db, cli
from app.models import User, Post, Role, Comment

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post, 'Comment': Comment, 'Role': Role}


if __name__ == '__main__':
    app.run()
