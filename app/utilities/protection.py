from functools import wraps
from flask import jsonify, make_response, request
from graphql import GraphQLError

def user_protected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers['Authorization'].split()[1]
        print(token)
        return func(*args, **kwargs)
    return wrapper
