from wagtail.images import get_image_model

import graphene

from wagtail_graphql.types import ImageObjectType


class ImageQueryMixin:
    images = graphene.List(ImageObjectType)

    def resolve_images(self, info):
        return get_image_model().objects.all()
