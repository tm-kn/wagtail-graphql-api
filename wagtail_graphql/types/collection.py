from wagtail.core.models import Collection
from wagtail.images import get_image_model

import graphene_django

from wagtail_graphql.types.images import ImageObjectType
from wagtail_graphql.types.structures import QuerySetList
from wagtail_graphql.utils import (
    exclude_restricted_collection_members, get_base_queryset_for_model_or_qs
)


class CollectionObjectType(graphene_django.DjangoObjectType):
    """
    GraphQL representation of the Wagtail's Collection model.
    """

    images = QuerySetList(ImageObjectType)

    class Meta:
        model = Collection
        only_fields = ('id', 'name')

    def resolve_images(self, info, **kwargs):
        """
        Resolve images belonging to a particular collection if privacy of the
        collection allows.
        """
        request = info.context
        qs = exclude_restricted_collection_members(
            request,
            get_image_model().objects.filter(collection_id=self.pk)
        )
        return get_base_queryset_for_model_or_qs(qs, info, **kwargs)
