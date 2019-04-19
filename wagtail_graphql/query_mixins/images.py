from wagtail.images import get_image_model

from wagtail_graphql.types import ImageObjectType, QuerySetList
from wagtail_graphql.utils import (
    exclude_restricted_collection_members, get_base_queryset_for_model_or_qs
)


class ImageQueryMixin:
    images = QuerySetList(ImageObjectType)

    def resolve_images(self, info, **kwargs):
        request = info.context
        return get_base_queryset_for_model_or_qs(
            exclude_restricted_collection_members(
                request, get_image_model().objects.all()
            ), info, **kwargs
        )
