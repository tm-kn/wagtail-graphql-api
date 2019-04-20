from django.utils.translation import ugettext_lazy as _

import graphene

from wagtail_graphql import settings
from wagtail_graphql.query_mixins import (
    CurrentSiteMixin, DocumentQueryMixin, ImageQueryMixin, PageQueryMixin,
    SnippetQueryMixin
)

# Allow enabling the images endpoint
if settings.WAGTAIL_GRAPHQL_ENABLE_IMAGES is True:
    image_query_mixin_cls = ImageQueryMixin
else:
    image_query_mixin_cls = type('DisabledImageQueryMixin')

# Allow enabling the documents endpoint
if settings.WAGTAIL_GRAPHQL_ENABLE_DOCUMENTS is True:
    documents_query_mixin_cls = DocumentQueryMixin
else:
    documents_query_mixin_cls = type('DisabledDocumentQueryMixin')


class WagtailQuery(
    graphene.ObjectType, PageQueryMixin, SnippetQueryMixin,
    image_query_mixin_cls, CurrentSiteMixin, documents_query_mixin_cls
):
    """
    Main GraphQL query used directly by the endpoint.
    """

    class Meta:
        description = _('Query Wagtail-related data.')


schema = graphene.Schema(query=WagtailQuery)
