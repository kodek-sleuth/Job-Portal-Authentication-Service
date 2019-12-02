from flask import Flask, request, session, redirect, make_response, jsonify
from flask_mongoengine import MongoEngine
from flask_graphql import GraphQLView
from app.schema import schema
from config import app_config
from app.helpers.google_auth import get_google_auth_data
from app.helpers.linkedin_auth import get_linkedin_auth_data, get_linkedin_auth_url

db = MongoEngine()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    db.init_app(app)

    # @app.route('/linkedin/auth', methods=['GET', 'POST'])
    # def linkedin_login():
    #     url = get_linkedin_auth_url()
    #     return redirect(url)
    #
    # @app.route('/',  methods=['GET', 'POST'])
    # def linked_callback():
    #     result = get_linkedin_auth_data()
    #     return make_response(jsonify(result), 201)

    @app.route('/google/auth', methods=['POST'])
    def google_login():
        result = get_google_auth_data()
        if 'error' in result.keys():
            return make_response(jsonify({'error': result['error']}), 500)
        return make_response(jsonify({'message': result['message']}), 200)

    app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
    return app
