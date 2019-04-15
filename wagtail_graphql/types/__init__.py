from wagtail_graphql.types.base import create_model_type
from wagtail_graphql.types.pages import PageInterface, create_page_type
from wagtail_graphql.types.snippets import create_snippet_type

__all__ = [
    'create_model_type', 'create_page_type', 'create_snippet_type',
    'PageInterface'
]
