from graphene import *
from flask import request
from graphene_mongo import MongoengineObjectType
from .model import User as UsersModel

class User(MongoengineObjectType):
    class Meta:
        model = UsersModel

class Query(ObjectType):
    users = List(User)

    def resolve_users(self, info):
        return list(UsersModel.objects.all())

