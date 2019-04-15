import graphene

from wagtail_graphql.query_mixins import PageQueryMixin, SnippetQueryMixin


class Query(graphene.ObjectType, PageQueryMixin, SnippetQueryMixin):
    pass


schema = graphene.Schema(query=Query)
