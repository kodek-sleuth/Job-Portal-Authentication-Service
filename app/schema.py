from graphene import Schema
import app.users.user_query
import app.users.user_mutations

class Query(app.users.user_query.Query):
    pass

class Mutations(app.users.user_mutations.Mutations):
    pass


schema = Schema(query=Query, mutation=Mutations)
