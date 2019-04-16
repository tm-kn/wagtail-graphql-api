from wagtail.images import get_image_model

import graphene
import graphene_django


class ImageInterface(graphene.Interface):
    pass


class ImageObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = get_image_model()
        only_fields = ('id', )
