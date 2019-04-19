from wagtail.core.fields import StreamField as WagtailStreamField

from graphene_django.converter import convert_django_field
from taggit.managers import TaggableManager

from wagtail_graphql.types import StreamField
from wagtail_graphql.types.structures import TagList


def convert_stream_field(field, _registry=None):
    return StreamField(description=field.help_text, required=not field.null)


def convert_tags_to_list_of_strings(field, _registry=None):
    return TagList(description=field.help_text, required=not field.null)


def register_converters():
    convert_django_field.register(WagtailStreamField, convert_stream_field)
    convert_django_field.register(
        TaggableManager, convert_tags_to_list_of_strings
    )
