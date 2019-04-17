from django.utils.translation import ugettext_lazy as _

import graphene

from wagtail_graphql.query_mixins import (
    ImageQueryMixin, PageQueryMixin, SnippetQueryMixin
)


class WagtailQuery(
    graphene.ObjectType, PageQueryMixin, SnippetQueryMixin, ImageQueryMixin
):
    class Meta:
        description = _('Query Wagtail-related data.')


schema = graphene.Schema(query=WagtailQuery)
