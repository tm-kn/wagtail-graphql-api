from django.utils.translation import ugettext_lazy as _

import graphene

from wagtail_graphql import settings
from wagtail_graphql.query_mixins import (
    CurrentSiteMixin, DocumentQueryMixin, ImageQueryMixin, PageQueryMixin,
    SnippetQueryMixin
)


class WagtailQuery(
    graphene.ObjectType, PageQueryMixin, SnippetQueryMixin,
    ImageQueryMixin, CurrentSiteMixin, DocumentQueryMixin
):
    """
    Main GraphQL query used directly by the endpoint.
    """

    class Meta:
        description = _('Query Wagtail-related data.')


schema = graphene.Schema(query=WagtailQuery)
