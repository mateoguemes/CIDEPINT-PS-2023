from flask import Flask , render_template_string
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def init_app(app):
    """This is the initiation of the app"""
    db.init_app(app)
    config_db(app)
    

def config_db(app):
    """This configures the DB to close the session when a request finishes"""
    @app.teardown_request
    def close_session(exception=None):
        db.session.close()

def reset_db():
    """This function deletes and recreates the DB to update the models' definitions"""
    db.drop_all()
    print("parece que anda")
    db.create_all()



