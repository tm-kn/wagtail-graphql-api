"""
wagtail-graphql-api
"""
from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField

__all__ = ['GraphQLEnabledModel', 'GraphQLField']

__version__ = "0.0.1a0"

default_app_config = 'wagtail_graphql.apps.WagtailGraphQLConfig'
