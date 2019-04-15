from wagtail.core.models import Page

import graphene

from wagtail_graphql.types.base import create_model_type
from wagtail_graphql.utils import get_base_queryset_for_page_model_or_qs


def create_page_type(model, fields):
    """
    Generate a DjangoObjectType for a Wagtail page.
    """
    return create_model_type(
        model, fields, meta_attrs={
            'interfaces': (PageInterface, ),
        }
    )


class PageInterface(graphene.Interface):
    """
    Set basic fields exposed on every single page object.
    """
    id = graphene.Int()
    depth = graphene.Int()
    page_type = graphene.String()
    title = graphene.String()
    seo_title = graphene.String()
    seo_description = graphene.String()
    show_in_menus = graphene.Boolean()
    children = graphene.List(lambda: PageInterface)
    siblings = graphene.List(lambda: PageInterface)
    parent = graphene.Field(lambda: PageInterface)
    next_siblings = graphene.List(lambda: PageInterface)
    previous_siblings = graphene.List(lambda: PageInterface)
    descendants = graphene.List(lambda: PageInterface)
    ancestors = graphene.List(lambda: PageInterface)

    def resolve_page_type(self, info):
        return '.'.join(
            [
                self.content_type.app_label,
                self.content_type.model_class().__name__
            ]
        )

    def resolve_children(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_children(), info
        )

    def resolve_descendants(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_children(), info
        )

    def resolve_ancestors(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_children(), info
        )

    def resolve_siblings(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_siblings().exclude(pk=self.pk), info
        )

    def resolve_next_siblings(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_next_siblings().exclude(pk=self.pk), info
        )

    def resolve_previous_siblings(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_previous_siblings().exclude(pk=self.pk), info
        )

    def resolve_parent(self, info):
        parent = self.get_parent()
        if parent is None:
            return
        qs = get_base_queryset_for_page_model_or_qs(Page, info)
        return qs.get(pk=parent.pk)

    def resolve_seo_title(self, info):
        return self.seo_title or self.title
