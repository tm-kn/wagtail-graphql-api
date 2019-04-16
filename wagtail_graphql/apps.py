from django import apps

from wagtail_graphql.checks import register_checks


class WagtailGraphQLConfig(apps.AppConfig):
    name = 'wagtail_graphql'

    def ready(self):
        register_checks()
