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
    others_kills = StringField(required=False, field=StringField)
    location = StringField(required=False)
    main_skill = StringField(required=False)

    @staticmethod
    def add_user(**kwargs):
        kwargs['password'] = bcrypt.generate_password_hash(kwargs['password'], 10)
        _user = User(**kwargs).save()
        return _user

    @staticmethod
    def display_users():
        users = User.objects
        return users

    @staticmethod
    def find_user(email, password):
        try:
            user = User.objects(__raw__={'email': email}).first()
            check_pwd = bcrypt.check_password_hash(user.password, password)
            if check_pwd:
                return user
            else:
                raise GraphQLError('wrong email or password')
        except:
            raise GraphQLError('wrong email or password')



