import graphene

from wagtail_graphql.query_mixins.pages import PageQueryMixin


class Query(graphene.ObjectType, PageQueryMixin):
    pass


schema = graphene.Schema(query=Query)
