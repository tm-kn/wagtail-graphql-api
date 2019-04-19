from django.utils.translation import ugettext_lazy as _

import graphene

from wagtail_graphql.inventory import inventory
from wagtail_graphql.query_mixins.base import (
    get_app_query_attributes, get_model_query_attributes_by_app
)
from wagtail_graphql.types import PositiveInt
from wagtail_graphql.utils import get_base_queryset_for_page_model_or_qs


def get_page_attributes_by_app():
    def resolve_pages_create(model):
        """
        Create a function to resolve all pages for a certain page model.
        """

        def resolve_pages(self, info, **kwargs):
            return get_base_queryset_for_page_model_or_qs(
                model, info, **kwargs
            )

        return resolve_pages

    return get_model_query_attributes_by_app(
        inventory.pages.graphql_types,
        resolve_objects_func=resolve_pages_create,
        field_arguments={
            'depth': graphene.Argument(
                PositiveInt, description=_('Depth in the page tree.')
            ),
            'show_in_menus': graphene.Argument(graphene.Boolean),
        }
    )


def get_pages_type():
    attrs = dict(
        get_app_query_attributes(get_page_attributes_by_app()),
        prefix='pages',
    )

    if not attrs:
        return

    class PagesByAppQueryMixinMeta:
        description = _(
            'Contains Django apps used by the registered GraphQL models.'
        )

    attrs['Meta'] = PagesByAppQueryMixinMeta
    return type('PagesByAppObjectType', (graphene.ObjectType, ), attrs)


def create_query_mixin():
    """Create the page query mixin dynamically."""

    class PageQueryMixinMeta:
        description = _('Object that contains all pages-related data.')

    pages_by_app_type = get_pages_type()

    if not pages_by_app_type:
        return type('EmptyPageQueryMixin')

    return type(
        'PageQueryMixin', tuple(), {
            'pages': graphene.Field(pages_by_app_type),
            'resolve_pages': lambda *args, **kwargs: True,
            'Meta': PageQueryMixinMeta
        }
    )


PageQueryMixin = create_query_mixin()
