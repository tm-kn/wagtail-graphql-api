import itertools
import logging

from django.utils.translation import ugettext_lazy as _

from wagtail.images import get_image_model
from wagtail.images.exceptions import InvalidFilterSpecError

import graphene
import graphene_django

from wagtail_graphql import settings
from wagtail_graphql.utils import resolve_absolute_url

logger = logging.getLogger(__name__)


def get_allowed_rendition_filters():
    return frozenset(
        itertools.chain(
            settings.WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS,
            [settings.WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER],
        )
    )


def get_default_rendition_filter():
    return settings.WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER


class RenditionInterface(graphene.Interface):
    """
    GraphQL interface for rendition object types.
    """
    id = graphene.ID()
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
    filter_spec = graphene.String()
    width = graphene.Int()
    height = graphene.Int()

    def resolve_id(self, info):
        return self.pk

    def resolve_url(self, info, absolute):
        """
        Resolve to an absolute URL if necessary.
        """
        request = info.context
        return resolve_absolute_url(self.url, request, absolute=absolute)


class RenditionObjectType(graphene_django.DjangoObjectType):
    """
    GraphQL representation of the image rendition model.
    """

    class Meta:
        model = get_image_model().get_rendition_model()
        interfaces = (RenditionInterface, )
        only_fields = ('id', )


class ImageInterface(graphene.Interface):
    """
    GraphQL interface for image object types.
    """

    id = graphene.ID()
    title = graphene.String()
    width = graphene.Int()
    height = graphene.Int()
    focal_point_x = graphene.Int()
    focal_point_y = graphene.Int()
    focal_point_width = graphene.Int()
    focal_point_height = graphene.Int()
    rendition = graphene.Field(
        RenditionObjectType,
        rendition_filter=graphene.Argument(
            graphene.String,
            name='filter',
            default_value=get_default_rendition_filter(),
            description=_('Wagtail rendition filter. One of: %s.') %
            (', '.join(get_allowed_rendition_filters()), )
        )
    )

    def resolve_id(self, info):
        return self.pk

    def resolve_rendition(self, info, rendition_filter):
        """
        Resolve an image rendition with a specified Wagtail's image rendition
        filter.

        Example:

        .. code::

           query {
               images {
                   rendition(filter: "fill-200x200") {
                       url
                   }
               }
           }

        """
        allowed = get_allowed_rendition_filters()

        if '*' not in allowed and rendition_filter not in allowed:
            msg = (
                f'Image filter "{rendition_filter}" is not allowed. It needs '
                f'to be one of: {", ".join(allowed)}.'
            )
            raise ValueError(msg)
        try:
            return self.get_rendition(rendition_filter)
        except InvalidFilterSpecError as e:
            msg = f'Image rendition filter "{rendition_filter}" is invalid.'
            raise ValueError(msg) from e


class ImageObjectType(graphene_django.DjangoObjectType):
    """
    GraphQL representation of Wagtail's image model.
    """

    class Meta:
        model = get_image_model()
        only_fields = ('id', )
        interfaces = (ImageInterface, )
