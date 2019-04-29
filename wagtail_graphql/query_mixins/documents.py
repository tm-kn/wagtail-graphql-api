from wagtail.documents.models import get_document_model

from graphql import GraphQLError

from wagtail_graphql import settings
from wagtail_graphql.types import DocumentObjectType, QuerySetList
from wagtail_graphql.utils import (
    exclude_restricted_collection_members, get_base_queryset_for_model_or_qs
)


class DocumentQueryMixin:
    documents = QuerySetList(DocumentObjectType)

    def resolve_documents(self, info, **kwargs):
        if settings.WAGTAIL_GRAPHQL_ENABLE_DOCUMENTS is not True:
            raise GraphQLError('Documents endpoint is disabled.')

        request = info.context
        return get_base_queryset_for_model_or_qs(
            exclude_restricted_collection_members(
                request, get_document_model().objects.all()
            ), info, **kwargs
        )
