import graphene
from crm.schema import Query
from crm.schema import Query, Mutation as CRMMutation


class Query(Query, graphene.ObjectType):
    pass
    
schema = graphene.Schema(query=Query)



class Query(Query, graphene.ObjectType):
    pass

class Mutation(CRMMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)