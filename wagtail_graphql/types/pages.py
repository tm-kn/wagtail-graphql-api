from django.utils.translation import ugettext_lazy as _

from wagtail.core.models import Page

import graphene

from wagtail_graphql.types.base import create_model_type
from wagtail_graphql.types.structures import QuerySetList
from wagtail_graphql.utils import get_base_queryset_for_page_model_or_qs


def create_page_type(model, fields):
    """
    Generate a DjangoObjectType subclass for a Wagtail page.
    """
    return create_model_type(
        model, fields, meta_attrs={
            'interfaces': (PageInterface, ),
        }
    )


class PageInterface(graphene.Interface):
    """
    Set basic fields exposed on every page object.
    """

    id = graphene.ID()
    url = graphene.String()
    depth = graphene.Int()
    page_type = graphene.String()
    title = graphene.String()
    seo_title = graphene.String()
    seo_description = graphene.String()
    show_in_menus = graphene.Boolean()
    specific = graphene.Field(lambda: PageInterface)
    children = QuerySetList(lambda: PageInterface, enable_search=True)
    siblings = QuerySetList(lambda: PageInterface, enable_search=True)
    parent = graphene.Field(lambda: PageInterface)
    next_siblings = QuerySetList(lambda: PageInterface, enable_search=True)
    previous_siblings = QuerySetList(lambda: PageInterface, enable_search=True)
    descendants = QuerySetList(lambda: PageInterface, enable_search=True)
    ancestors = QuerySetList(lambda: PageInterface, enable_search=True)

    class Meta:
        description = _(
            'Interface used by every GraphQL Wagtail page object type.'
        )

    def resolve_url(self, info):
        """
        Resolve a path to a page.
        """
        request = info.context
        return self.get_url(request=request, current_site=request.site)

    def resolve_page_type(self, info):
        """
        Resolve a page type in a form of ``app.ModelName``.
        """
        return '.'.join(
            [
                self.content_type.app_label,
                self.content_type.model_class().__name__
            ]
        )

    def resolve_children(self, info, **kwargs):
        return get_base_queryset_for_page_model_or_qs(
            self.get_children(), info, **kwargs
        )

    def resolve_descendants(self, info, **kwargs):
        return get_base_queryset_for_page_model_or_qs(
            self.get_descendants(), info, **kwargs
        )

    def resolve_ancestors(self, info, **kwargs):
        return get_base_queryset_for_page_model_or_qs(
            self.get_ancestors(), info, **kwargs
        )

    def resolve_siblings(self, info, **kwargs):
        return get_base_queryset_for_page_model_or_qs(
            self.get_siblings().exclude(pk=self.pk), info, **kwargs
        )

    def resolve_next_siblings(self, info, **kwargs):
        return get_base_queryset_for_page_model_or_qs(
            self.get_next_siblings().exclude(pk=self.pk), info, **kwargs
        )

    def resolve_previous_siblings(self, info, **kwargs):
        return get_base_queryset_for_page_model_or_qs(
            self.get_prev_siblings().exclude(pk=self.pk), info, **kwargs
        )

    def resolve_parent(self, info, **kwargs):
        parent = self.get_parent()
        if parent is None:
            return
        qs = get_base_queryset_for_page_model_or_qs(Page, info, **kwargs)
        try:
            return qs.get(pk=parent.pk).specific
        except Page.DoesNotExist:
            return

    def resolve_specific(self, info, **kwargs):
        return self.specific

    def resolve_seo_title(self, info):
        """
        Get page's SEO title. Fallback to a normal page's title if absent.
        """
        return self.seo_title or self.title
