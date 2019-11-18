import sys
import re
from functools import wraps

from graphql import GraphQLError
from flask import request, jsonify, make_response


def validate_create_user_mutation(func):
    """Decorator to validate creation of a user"""
    from app.users.model import User

    @wraps(func)
    def wrapper(*args, **kwargs):

        user = User.objects(__raw__={'email': kwargs['email']}).first()
        if user and user.email:
            raise GraphQLError('please use a different email')
        try:
            return func(*args, **kwargs)
        except Exception as error:
            raise GraphQLError(error)

    return wrapper

def regex(name):
    if name == "name_regex":
        name_regex = re.compile("^[a-zA-Z]+(([',. -][a-zA-Z ])?[a-zA-Z]*)*$")
        return name_regex

    elif name == "password_regex":
        password_regex = re.compile("^.*(?=.{8,})((?=.*[!@#$%^&*()\-_=+{};:,<.>])"
                                    "{1})(?=.*\d)((?=.*[a-z]){1})((?=.*[A-Z]){1}).*$")
        return password_regex

    elif name == "phone_regex":
        phone_number_regex = re.compile("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$")
        return phone_number_regex

    elif name == "url_regex":
        url_regex = re.compile("^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?"
                               "[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$")
        return url_regex

    elif name == "email_regex":
        email_regex = re.compile("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return email_regex









