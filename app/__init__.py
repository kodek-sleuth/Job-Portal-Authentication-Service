from flask import Flask
from flask_mongoengine import MongoEngine
from flask_graphql import GraphQLView
from app.schema import schema

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config['MONGODB_SETTINGS'] = {
        'db': 'business',
        'host': 'localhost',
        'port': 27017
    }
    app.config['SECRET_KEY'] = "thisisaverybadopensecret"

    db.init_app(app)

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql',
                                                               schema=schema, graphiql=True))
    return app
