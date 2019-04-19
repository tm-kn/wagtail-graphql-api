import collections

import graphene

from wagtail_graphql.types import QuerySetList


def get_model_query_attributes_by_app(
    graphql_types, resolve_objects_func, field_arguments=None
):
    """
    Segregate model object types by app and generate attributes for
    the query object.
    """
    by_app = collections.defaultdict(lambda: {})

    if field_arguments is None:
        field_arguments = {}

    for model, object_type in graphql_types:
        attrs = {}
        app_label = model._meta.app_label
        # Define a field name that will be used by the GraphQL
        # query.
        field_name = model.__name__
        field_name = field_name[0].lower() + field_name[1:]

        # Define a GraphQL data type for that specific model type.
        attrs[field_name] = QuerySetList(
            object_type,
            name=field_name,
            **field_arguments,
        )

        # Add a method to resolve all instances for a certain model type.
        attrs[f'resolve_{field_name}'] = resolve_objects_func(model)
        by_app[app_label].update(attrs)

    return by_app.items()


def get_app_query_attributes(by_app_attributes, prefix=''):
    for app, attrs in by_app_attributes:
        field_name = app
        yield field_name, graphene.Field(
            type(
                f'{field_name.capitalize()}{prefix.capitalize()}'
                'AppQueryObjectType', (graphene.ObjectType, ), attrs
            )
        )
        yield f'resolve_{field_name}', lambda *args, **kwargs: True
