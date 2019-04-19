from wagtail.documents.models import get_document_model

from wagtail_graphql.types import DocumentObjectType, QuerySetList
from wagtail_graphql.utils import (
    exclude_restricted_collection_members, get_base_queryset_for_model_or_qs
)


class DocumentQueryMixin:
    documents = QuerySetList(DocumentObjectType)

    def resolve_documents(self, info, **kwargs):
        request = info.context
        return get_base_queryset_for_model_or_qs(
            exclude_restricted_collection_members(
                request, get_document_model().objects.all()
            ), info, **kwargs
        )
