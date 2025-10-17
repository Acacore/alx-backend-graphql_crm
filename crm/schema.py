import graphene
from graphene_django import DjangoObjectType

from crm.models import *

class CRMQuery(graphene.ObjectType):
    hello = graphene.String()

    def resolve_hello(root, info):
        return "Hello, GraphQL!"
    
