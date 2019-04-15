import graphene

from wagtail_graphql.inventory import inventory


def resolve_snippets_create(model):
    """
    Create a function to resolve all pages for a certain snippet model.
    """

    def resolve_pages(self, info):
        # This is highly insecure if you want to keep your snippet data hidden
        # from the public.
        return model.objects.all()

    return resolve_pages


def get_snippet_types():
    """
    Generate GraphQL page types dynamically.
    """
    for model, object_type in inventory.snippets.graphql_types:
        # Define a field name that will be used by the GraphQL
        # query.
        field_name = (f'snippets_{model._meta.app_label}_{model.__name__}')

        # Define a GraphQL data type for that specific page type.
        yield field_name, graphene.List(object_type, name=field_name)

        # Add a method to resolve all instances for a certain model.
        yield f'resolve_{field_name}', resolve_snippets_create(model)


# Create a query mixin dynamically.
SnippetQueryMixin = type('SnippetQueryMixin', tuple(),
                         dict(get_snippet_types()))
