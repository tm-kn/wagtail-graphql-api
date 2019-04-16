import graphene

from wagtail_graphql.query_mixins import (ImageQueryMixin, PageQueryMixin,
                                          SnippetQueryMixin)


class Query(
    graphene.ObjectType, PageQueryMixin, SnippetQueryMixin, ImageQueryMixin
):
    pass


schema = graphene.Schema(query=Query)
