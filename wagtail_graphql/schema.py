import graphene

from wagtail_graphql.mixins import PageQueryMixin


class Query(graphene.ObjectType, PageQueryMixin):
    pass


schema = graphene.Schema(query=Query)
