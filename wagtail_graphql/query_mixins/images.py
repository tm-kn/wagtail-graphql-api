from wagtail.images import get_image_model

from wagtail_graphql.types import ImageObjectType
from wagtail_graphql.types import QuerySetList
from wagtail_graphql.utils import get_base_queryset_for_model_or_qs


class ImageQueryMixin:
    images = QuerySetList(ImageObjectType)

    def resolve_images(self, info, **kwargs):
        return get_base_queryset_for_model_or_qs(
            get_image_model().objects.all(), info, **kwargs
        )
