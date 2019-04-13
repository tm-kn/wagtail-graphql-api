from wagtail.core.models import Page

import graphene
import graphene_django

from wagtail_graphql.inventory import inventory
from wagtail_graphql.utils import get_base_queryset_for_page_model_or_qs


class PageInterface(graphene.Interface):
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
    descdendants = graphene.List(lambda: PageInterface)
    ancestors = graphene.List(lambda: PageInterface)

    def resolve_page_type(self, info):
        return '.'.join([
            self.content_type.app_label,
            self.content_type.model_class().__name__
        ])

    def resolve_children(self, info):
        return get_base_queryset_for_page_model_or_qs(self.get_children(),
                                                      info)

    def resolve_descendants(self, info):
        return get_base_queryset_for_page_model_or_qs(self.get_children(),
                                                      info)

    def resolve_ancestors(self, info):
        return get_base_queryset_for_page_model_or_qs(self.get_children(),
                                                      info)

    def resolve_siblings(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_siblings().exclude(pk=self.pk), info)

    def resolve_next_siblings(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_next_siblings().exclude(pk=self.pk), info)

    def resolve_previous_siblings(self, info):
        return get_base_queryset_for_page_model_or_qs(
            self.get_previous_siblings().exclude(pk=self.pk), info)

    def resolve_parent(self, info):
        parent = self.get_parent()
        if parent is None:
            return
        qs = get_base_queryset_for_page_model_or_qs(Page, info)
        return qs.get(pk=parent.pk)

    def resolve_seo_title(self, info):
        return self.seo_title or self.title


def create_page_type(model):
    def get_meta(model):
        fields = inventory.get_page_model_fields_for(model)
        return type('Meta', tuple(), {
            'model': model,
            'interfaces': (PageInterface, ),
            'only_fields': tuple([field.name for field in fields]) or ('id', ),
        })

    return type(
        f'{model.__name__}ObjectType',
        (graphene_django.DjangoObjectType, ),
        {
            'Meta': get_meta(model)
        }
    )


def resolve_pages_create(model):
    def resolve_pages(self, info):
        return get_base_queryset_for_page_model_or_qs(model, info)
    return resolve_pages


def get_page_types():
    for page_model in inventory.page_models:
        field_name = (
            f"pages_{page_model._meta.app_label}_{page_model._meta.model_name}"
        )
        yield field_name, graphene.List(create_page_type(page_model))
        yield f'resolve_{field_name}', resolve_pages_create(page_model)


PageQueryMixin = type('PageQueryMixin', tuple(), dict(get_page_types()))
