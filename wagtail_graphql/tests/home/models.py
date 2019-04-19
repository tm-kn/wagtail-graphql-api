from wagtail.core.models import Page

from wagtail_graphql import GraphQLEnabledPage


class HomePage(GraphQLEnabledPage, Page):
    pass
