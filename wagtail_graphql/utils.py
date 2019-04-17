import inspect

from django.db import models

from wagtail.core.models import PageViewRestriction
from wagtail.search.models import Query

from wagtail.search.queryset import SearchableQuerySetMixin
from wagtail_graphql import settings


def exclude_invisible_pages(request, pages):
    """
    Excludes from the QuerySet pages that are invisible
    for a current user.
    """

    # Make sure pages are live
    pages = pages.live()

    # Get list of pages that are restricted to this user
    restricted_pages = [
        restriction.page for restriction in
        PageViewRestriction.objects.all().select_related('page')
        if not restriction.accept_request(request)
    ]

    # Exclude the restricted pages and their descendants from the queryset
    for restricted_page in restricted_pages:
        pages = pages.not_descendant_of(restricted_page, inclusive=True)

    return pages


def resolve_queryset(qs, info, **kwargs):
    """
    Add limit, offset and search capabilities to the query.
    """
    limit = kwargs.get('limit')
    offset = int(kwargs.get('offset', 0))
    search_query = kwargs.get('search_query', 0)

    if search_query:
        # Check if the queryset is searchable using Wagtail search.
        if not isinstance(qs, SearchableQuerySetMixin):
            raise TypeError("This data type is not searchable by Wagtail.")
        if settings.WAGTAIL_GRAPHQL_ADD_SEARCH_HIT:
            query = Query.get(search_query)
            query.add_hit()
        return qs.search(search_query)

    if limit is not None:
        limit = int(limit)
        qs = qs[offset:limit + offset]

    return qs


def get_base_queryset_for_page_model_or_qs(page_model_or_qs, info, **kwargs):
    request = info.context
    if inspect.isclass(page_model_or_qs) \
            and issubclass(page_model_or_qs, models.Model):
        qs = page_model_or_qs.objects.all()
    else:
        qs = page_model_or_qs.all()

    qs = exclude_invisible_pages(request, qs)
    qs = qs.select_related('content_type')

    return resolve_queryset(qs, info, **kwargs)
