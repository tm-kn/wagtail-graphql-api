"""
wagtail-graphql-api
"""
import inspect

import django

import graphene_django

from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField

__all__ = ['GraphQLEnabledModel', 'GraphQLField']

__version__ = "0.0.1a0"

default_app_config = 'wagtail_graphql.apps.WagtailGraphQLConfig'


def lazy_model_type(model):
    """
    Get GraphQL type for a Django model lazily.

    It can be used together with GraphQL fields and scalars, e.g.

    * ``graphene.Field(lazy_model_type(ModelA))``
    * ``graphene.List(lazy_model_type('someapp.ModelB'))``
    * ``graphene.Field(lazy_model_type(lambda: ModelC))
    """
    def get_model():
        if inspect.isclass(model):
            return model

        if isinstance(model, str):
            return django.apps.apps.get_model(model)

        if callable(model):
            return model()

    return lambda: graphene_django.registry.get_global_registry() \
                                           .get_type_for_model(get_model())


def lazy_queryset_list(model, **kwargs):
    def inner():
        from wagtail_graphql.types import QuerySetList
        return QuerySetList(lazy_model_type(model), **kwargs)
    return inner
