import collections

import graphene

from wagtail_graphql.types import QuerySetList


def get_model_query_attributes_by_app(graphql_types, resolve_objects_func):
    """
    Segregate model object types by app and generate attributes for
    the query mixin.
    """
    by_app = collections.defaultdict(lambda: {})

    for model, object_type in graphql_types:
        attrs = {}
        app_label = model._meta.app_label
        # Define a field name that will be used by the GraphQL
        # query.
        field_name = model.__name__

        # Define a GraphQL data type for that specific model type.
        attrs[field_name] = QuerySetList(
            object_type,
            name=field_name,
        )

        # Add a method to resolve all instances for a certain model type.
        attrs[f'resolve_{field_name}'] = resolve_objects_func(model)
        by_app[app_label].update(attrs)

    return by_app.items()


def get_app_query_attributes(by_app_attributes):
    for app, attrs in by_app_attributes:
        field_name = app
        yield field_name, graphene.Field(
            type(
                f'{field_name.capitalize()}AppQueryMixin',
                (graphene.ObjectType, ), attrs
            )
        )
        yield f'resolve_{field_name}', lambda *args, **kwargs: True
