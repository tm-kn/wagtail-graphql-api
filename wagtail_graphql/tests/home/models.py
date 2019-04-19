from wagtail.core.models import Page

from wagtail_graphql import GraphQLEnabledModel


class HomePage(GraphQLEnabledModel, Page):
    pass
