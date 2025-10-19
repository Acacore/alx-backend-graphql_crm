from django.urls import path
from .views import *
from .schema import schema
from graphene_django.views import GraphQLView


urlpatterns = [
    path('', index),
    path("graphql", GraphQLView.as_view(graphiql=True, schema=schema))
    
]