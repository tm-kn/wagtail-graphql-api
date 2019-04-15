from wagtail_graphql.types.base import create_model_type


def create_snippet_type(model, fields):
    """
    Generate a DjangoObjectType for a Wagtail page.
    """
    return create_model_type(model, fields)
