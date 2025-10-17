import graphene
from crm.schema import CRMQuery


class Query(CRMQuery, graphene.ObjectType):
    ...
    
schema = graphene.Schema(query=Query)