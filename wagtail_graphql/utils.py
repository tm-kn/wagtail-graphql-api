import inspect

from django.db import models

from wagtail.core.models import PageViewRestriction
from wagtail.search.backends import get_search_backend
from wagtail.search.index import class_is_indexed
from wagtail.search.models import Query

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
        if not class_is_indexed(qs.model):
            raise TypeError("This data type is not searchable by Wagtail.")

        if settings.WAGTAIL_GRAPHQL_ADD_SEARCH_HIT is True:
            query = Query.get(search_query)
            query.add_hit()

        return get_search_backend().search(search_query, qs)

    if limit is not None:
        limit = int(limit)
        qs = qs[offset:limit + offset]

    return qs


def model_to_qs(model_or_qs):
    if inspect.isclass(model_or_qs) \
            and issubclass(model_or_qs, models.Model):
        qs = model_or_qs.objects.all()
    else:
        qs = model_or_qs.all()
    return qs


def get_base_queryset_for_model_or_qs(model_or_qs, info, **kwargs):
    qs = model_to_qs(model_or_qs)
    return resolve_queryset(qs, info, **kwargs)


def get_base_queryset_for_page_model_or_qs(page_model_or_qs, info, **kwargs):
    request = info.context
    page_qs = model_to_qs(page_model_or_qs)

    # Only display pages for the current request's site.
    page_qs = page_qs.in_site(request.site)

    page_qs = exclude_invisible_pages(request, page_qs)
    page_qs = page_qs.select_related('content_type')
    return resolve_queryset(page_qs, info, **kwargs)
