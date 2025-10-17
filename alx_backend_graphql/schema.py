import graphene
from graphene_django import DjangoObjectType

from crm.models import *

class Query(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"
    
schema = graphene.schema(query=Query)