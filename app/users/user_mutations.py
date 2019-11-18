import re
import jwt
from graphene import *
from graphql import GraphQLError
from flask import request, current_app
from graphene_mongo import MongoengineObjectType
from app.users.user_query import User
from app.users.model import User as UserModel
from app.utilities.validators import validate_create_user_mutation

class CreateUser(Mutation):
    name = String()
    email = String()
    message = String()

    class Arguments:
        name = String()
        email = String()
        password = String()

    @validate_create_user_mutation
    def mutate(self, info, **kwargs):
        user = UserModel.add_user(**kwargs)
        return CreateUser(name=user.name, email=user.email, message="you have successfully signed up")

class LoginUser(Mutation):
    message = String()
    token = String()

    class Arguments:
        email = String()
        password = String()

    def mutate(self, info, **kwargs):
        user = UserModel.find_user(kwargs["email"], kwargs["password"])
        if user is not None:
            message = 'successfully logged in'
            token = jwt.encode(kwargs, current_app.config['SECRET_KEY'], algorithm="HS256")
            return LoginUser(token=token, message=message)
        else:
            raise GraphQLError('wrong username or password')


class Mutations(ObjectType):
    login_user = LoginUser.Field()
    create_user = CreateUser.Field()
