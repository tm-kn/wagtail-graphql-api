from wagtail.core.fields import StreamField as WagtailStreamField

from graphene_django.converter import convert_django_field

from wagtail_graphql.types import StreamField


def convert_stream_field(field, _registry=None):
    return StreamField(
        description=field.help_text, required=not field.null
    )


def register_converters():
    convert_django_field.register(WagtailStreamField, convert_stream_field)
