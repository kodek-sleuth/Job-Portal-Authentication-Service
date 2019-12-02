import re

from mongoengine.document import Document
from mongoengine.fields import *
from flask_bcrypt import Bcrypt
from graphql import GraphQLError
from flask import current_app

from app.utilities.validators import regex

bcrypt = Bcrypt()

class User(Document):
    name = StringField(required=True, min_length=1, regex=regex("name_regex"))
    email = StringField(required=True, unique=True, regex=regex("email_regex"))
    password = StringField(required=True, min_length=8, regex=regex("password_regex"))
    telephone = IntField(required=False, min_length=10, regex=regex("phone_number_regex"))
    resume = StringField(required=False, regex=regex("url_regex"))
    bio = StringField(required=False, min_length=10, max_length=500)
    other_skills = StringField(required=False, field=StringField)
    picture = StringField(required=False, default="https://image.flaticon.com/icons/svg/145/145846.svg")
    is_verified = BooleanField(default=False)
    location = StringField(required=False)
    main_skill = StringField(required=False)

    @staticmethod
    def add_user(**kwargs):
        try:
            user_in_db = User.objects(email=kwargs['email']).first()
            if user_in_db:
                raise GraphQLError('email is already registered')
            else:
                kwargs['password'] = bcrypt.generate_password_hash(kwargs['password'], 10)
                _user = User(**kwargs).save()
                return _user
        except Exception as error:
            raise GraphQLError(error)


    @staticmethod
    def display_users():
        users = User.objects
        return users

    @staticmethod
    def find_user(email, password):
        try:
            user = User.objects(email=email).first()
            check_pwd = bcrypt.check_password_hash(user.password, password)
            if check_pwd:
                return user
            else:
                return {'error': 'wrong email or password'}
        except:
            return {'error': 'wrong email or password'}
