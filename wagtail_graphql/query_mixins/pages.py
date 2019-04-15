import graphene

from wagtail_graphql.inventory import inventory
from wagtail_graphql.utils import get_base_queryset_for_page_model_or_qs


def resolve_pages_create(model):
    """
    Create a function to resolve all pages for a certain page model.
    """

    def resolve_pages(self, info):
        return get_base_queryset_for_page_model_or_qs(model, info)

    return resolve_pages


def get_page_types():
    """
    Generate GraphQL page types dynamically.
    """
    for page_model, object_type in inventory.pages.page_graphql_types:
        # Define a field name that will be used by the GraphQL
        # query.
        field_name = (f'pages_{page_model._meta.app_label}_'
                      f'{page_model.__class__.__name__}')

        # Define a GraphQL data type for that specific page type.
        yield field_name, graphene.List(object_type, name=field_name)

        # Add a method to resolve all instances for a certain page model.
        yield f'resolve_{field_name}', resolve_pages_create(page_model)


# Create a query mixin dynamically.
PageQueryMixin = type('PageQueryMixin', tuple(), dict(get_page_types()))
