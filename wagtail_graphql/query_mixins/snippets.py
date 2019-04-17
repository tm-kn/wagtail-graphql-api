import graphene

from wagtail_graphql.inventory import inventory
from wagtail_graphql.types import QuerySetList
from wagtail_graphql.utils import get_base_queryset_for_model_or_qs


def resolve_snippets_create(model):
    """
    Create a function to resolve all pages for a certain snippet model.
    """

    def resolve_snippets(self, info, **kwargs):
        # This is highly insecure if you want to keep your snippet data hidden
        # from the public.
        return get_base_queryset_for_model_or_qs(model, info, **kwargs)

    return resolve_snippets


def get_snippet_types():
    """
    Generate GraphQL page types dynamically.
    """
    for model, object_type in inventory.snippets.graphql_types:
        # Define a field name that will be used by the GraphQL
        # query.
        field_name = (f'snippets_{model._meta.app_label}_{model.__name__}')

        # Define a GraphQL data type for that specific page type.
        yield field_name, QuerySetList(object_type, name=field_name)

        # Add a method to resolve all instances for a certain model.
        yield f'resolve_{field_name}', resolve_snippets_create(model)


# Create a query mixin dynamically.
SnippetQueryMixin = type('SnippetQueryMixin', tuple(),
                         dict(get_snippet_types()))
