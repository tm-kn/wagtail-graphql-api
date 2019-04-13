import graphene

from wagtail_graphql.inventory import inventory
from wagtail_graphql.types.pages import create_page_type
from wagtail_graphql.utils import get_base_queryset_for_page_model_or_qs


def resolve_pages_create(model):
    def resolve_pages(self, info):
        return get_base_queryset_for_page_model_or_qs(model, info)

    return resolve_pages


def get_page_types():
    """
    Generate page types dynamically.
    """
    for page_model in inventory.page_models:
        object_type = create_page_type(
            page_model, inventory.get_page_model_fields_for(page_model))
        field_name = (
            f"pages_{page_model._meta.app_label}_{page_model._meta.model_name}"
        )
        yield field_name, graphene.List(object_type)
        yield f'resolve_{field_name}', resolve_pages_create(page_model)


PageQueryMixin = type('PageQueryMixin', tuple(), dict(get_page_types()))
