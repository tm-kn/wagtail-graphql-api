from django.utils.translation import ugettext_lazy as _

from wagtail.documents.models import get_document_model

import graphene
import graphene_django

from wagtail_graphql.utils import resolve_absolute_url


class DocumentObjectType(graphene_django.DjangoObjectType):
    """
    Represent the Wagtail's Document model as a GraphQL type.
    """
    url = graphene.String(
        absolute=graphene.Argument(
            graphene.Boolean,
            description=_(
                'Make the URL absolute if the static path is relative.'
            ),
            default_value=True
        )
    )

    class Meta:
        model = get_document_model()
        only_fields = ('id', 'title', 'file_size')

    def resolve_url(self, info, absolute):
        request = info.context
        return resolve_absolute_url(self.url, request, absolute=absolute)
