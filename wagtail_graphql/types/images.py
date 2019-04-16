import urllib

from django.utils.translation import ugettext_lazy as _

from wagtail.images import get_image_model

import graphene
import graphene_django


class RenditionInterface(graphene.Interface):
    id = graphene.Int()
    alt = graphene.String()
    url = graphene.String(
        absolute=graphene.Argument(
            graphene.Boolean,
            description=_(
                'Make the URL absolute if the static path is relative.'
            ),
            default_value=True
        )
    )

    def resolve_id(self, info):
        return self.pk

    def resolve_url(self, info, absolute):
        if not absolute or urllib.parse.urlparse(self.url).netloc:
            return self.url

        return info.context.build_absolute_uri(self.url)


class RenditionObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = get_image_model().get_rendition_model()
        interfaces = (RenditionInterface, )
        only_fields = ('id', )


class ImageInterface(graphene.Interface):
    id = graphene.Int()
    title = graphene.String()
    width = graphene.Int()
    height = graphene.Int()
    focal_point_x = graphene.Int()
    focal_point_y = graphene.Int()
    focal_point_width = graphene.Int()
    focal_point_height = graphene.Int()
    rendition = graphene.Field(
        RenditionObjectType,
        filter=graphene.Argument(
            graphene.String,
            default_value='original',
            description=_('Wagtail rendition filter')
        )
    )

    def resolve_id(self, info):
        return self.pk

    def resolve_rendition(self, info, filter):
        return self.get_rendition(filter)


class ImageObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = get_image_model()
        only_fields = ('id', )
        interfaces = (ImageInterface, )
