from django.utils.translation import ugettext_lazy as _

import graphene

from wagtail_graphql.inventory import inventory
from wagtail_graphql.query_mixins.base import (
    get_app_query_attributes, get_model_query_attributes_by_app
)
from wagtail_graphql.utils import get_base_queryset_for_model_or_qs


def get_snippets_attributes_by_app():
    def resolve_snippets_create(model):
        """
        Create a function to resolve all instances for a certain
        snippet model.
        """

        def resolve_snippets(self, info, **kwargs):
            return get_base_queryset_for_model_or_qs(
                model, info, **kwargs
            )

        return resolve_snippets

    return get_model_query_attributes_by_app(
        inventory.snippets.graphql_types,
        resolve_objects_func=resolve_snippets_create
    )


def get_snippets_type():
    attrs = dict(get_app_query_attributes(get_snippets_attributes_by_app()))

    class SnippetByAppQueryMixinMeta:
        description = _(
            'Contains Django apps used by the registered GraphQL models.'
        )

    attrs['Meta'] = SnippetByAppQueryMixinMeta
    return type('SnippetByAppQueryMixin', (graphene.ObjectType, ), attrs)


class SnippetQueryMixinMeta:
    description = _('Object that contains all snippet-related data.')


# Create a query mixin dynamically.
SnippetQueryMixin = type(
    'SnippetQueryMixin', tuple(), {
        'snippets': graphene.Field(get_snippets_type()),
        'resolve_snippets': lambda *args, **kwargs: True,
        'Meta': SnippetQueryMixinMeta
    }
)
