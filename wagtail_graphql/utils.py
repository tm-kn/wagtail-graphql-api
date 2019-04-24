import inspect
import urllib

from django.db import models

from wagtail.core.models import (
    Collection, CollectionViewRestriction, PageViewRestriction
)
from wagtail.search.backends import get_search_backend
from wagtail.search.index import class_is_indexed
from wagtail.search.models import Query

from wagtail_graphql import settings


def exclude_restricted_collection_members(request, collection_members):
    """
    Filter out a list of Wagtail collection members (e.g. images or
    documents) that have collection privacy set accordingly.

    :param request: Request used to authorize access to pages.
    :type request: django.http.request.HttpRequest
    :param pages: QuerySet containing pages to filter.
    """
    restricted_collections = [
        restriction.collection for restriction in
        CollectionViewRestriction.objects.all().select_related('collection')
        if not restriction.accept_request(request)
    ]

    collections = Collection.objects.all()

    for restricted_collection in restricted_collections:
        collections = collections.not_descendant_of(
            restricted_collection, inclusive=True
        )

    return collection_members.filter(
        collection_id__in=collections.values_list('pk', flat=True)
    )


def exclude_invisible_pages(request, pages):
    """
    Exclude from the QuerySet of pages that are invisible
    for the current user.

    :param request: Request used to authorize access to pages.
    :type request: django.http.request.HttpRequest
    :param pages: QuerySet containing pages to filter.
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


def resolve_queryset(
    qs,
    info,
    limit=None,
    offset=None,
    search_query=None,
    id=None,
    order=None,
    **kwargs
):
    """
    Add limit, offset and search capabilities to the query. This contains
    argument names used by
    :class:`~wagtail_graphql.types.structures.QuerySetList`.

    :param qs: Query set to be modified.
    :param info: Graphene's info object.
    :param limit: Limit number of objects in the QuerySet.
    :type limit: int
    :param id: Filter by the primary key.
    :type limit: int
    :param offset: Omit a number of objects from the beggining of the query set
    :type offset: int
    :param search_query: Using wagtail search exclude objects that do not match
                         the search query.
    :type search_query: str
    :param order: Use Django ordering format to order the query set.
    :type order: str
    """
    offset = int(offset or 0)

    if id is not None:
        qs = qs.filter(pk=id)

    if id is None and search_query:
        # Check if the queryset is searchable using Wagtail search.
        if not class_is_indexed(qs.model):
            raise TypeError("This data type is not searchable by Wagtail.")

        if settings.WAGTAIL_GRAPHQL_ADD_SEARCH_HIT is True:
            query = Query.get(search_query)
            query.add_hit()

        return get_search_backend().search(search_query, qs)

    if order is not None:
        qs = qs.order_by(*map(lambda x: x.strip(), order.split(',')))

    if limit is not None:
        limit = int(limit)
        qs = qs[offset:limit + offset]

    return qs


def model_to_qs(model_or_qs):
    """
    Convert model to a query set if it is not already a query set.

    :param model_or_qs: Model or query set to be cast as a query set.
    """
    if inspect.isclass(model_or_qs) \
            and issubclass(model_or_qs, models.Model):
        qs = model_or_qs.objects.all()
    else:
        qs = model_or_qs.all()
    return qs


def get_base_queryset_for_model_or_qs(model_or_qs, info, **kwargs):
    """
    Process a query set before displaying it in the GraphQL query result.

    :param model_or_qs: Model or a query set to be transformer.
    :param info: Graphene's info object.
    :param kwargs: Any additional keyword arguments passed from the GraphQL
                   query.
    """
    qs = model_to_qs(model_or_qs)
    return resolve_queryset(qs, info, **kwargs)


def get_base_queryset_for_page_model_or_qs(page_model_or_qs, info, **kwargs):
    """
    The same as :func:`get_base_queryset_for_model_or_qs`,
    except it adds Wagtail page-specific filters and privacy checks.

    :param model_or_qs: Model or a query set to be transformer.
    :param info: Graphene's info object.
    :param kwargs: Any additional keyword arguments passed from the GraphQL
                   query.
    """
    request = info.context
    page_qs = model_to_qs(page_model_or_qs)

    # Add filtering by depth
    depth = kwargs.get('depth')
    if depth is not None:
        page_qs = page_qs.filter(depth=depth)

    # Add filtering by "show in menus"
    depth = kwargs.get('show_in_menus')
    if depth is not None:
        page_qs = page_qs.filter(show_in_menus=True)

    # Only display pages for the current request's site.
    page_qs = page_qs.in_site(request.site)

    page_qs = exclude_invisible_pages(request, page_qs)
    page_qs = page_qs.select_related('content_type')
    return resolve_queryset(page_qs, info, **kwargs)


def resolve_absolute_url(url, request, absolute=True):
    """
    Transform URL to an absolute one if it already is not absolute.

    :param url: The URL to be resolved, relative or absolute.
    :type url: str
    :param request: Request used to get the domain.
    :type request: django.http.request.HttpRequest
    :param absolute: Set to ``True`` if value should be returned as absolute.
    :type absolute: bool
    """
    if request is None or not absolute or urllib.parse.urlparse(url).netloc:
        return url

    return request.build_absolute_uri(url)
