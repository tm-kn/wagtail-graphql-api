from django import apps


class WagtailGraphQLConfig(apps.AppConfig):
    name = 'wagtail_graphql'

    def ready(self):
        from wagtail_graphql.checks import register_checks
        from wagtail_graphql.converters import register_converters

        register_checks()
        register_converters()
