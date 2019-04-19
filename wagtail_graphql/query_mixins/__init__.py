from wagtail_graphql.query_mixins.documents import DocumentQueryMixin
from wagtail_graphql.query_mixins.images import ImageQueryMixin
from wagtail_graphql.query_mixins.pages import PageQueryMixin
from wagtail_graphql.query_mixins.sites import CurrentSiteMixin
from wagtail_graphql.query_mixins.snippets import SnippetQueryMixin

__all__ = [
    'CurrentSiteMixin',
    'ImageQueryMixin',
    'PageQueryMixin',
    'SnippetQueryMixin',
    'DocumentQueryMixin',
]
