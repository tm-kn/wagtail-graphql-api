import inspect

from django.db import models

from wagtail.core.models import PageViewRestriction


def exclude_invisible_pages(request, pages):
    """
    Excludes from the QuerySet pages that are invisible
    for a current user.
    """

    # Make sure pages are live
    pages = pages.live()

    # Get list of pages that are restricted to this user
    restricted_pages = [
        restriction.page
        for restriction
        in PageViewRestriction.objects.all().select_related('page')
        if not restriction.accept_request(request)
    ]

    # Exclude the restricted pages and their descendants from the queryset
    for restricted_page in restricted_pages:
        pages = pages.not_descendant_of(restricted_page, inclusive=True)

    return pages


def get_base_queryset_for_page_model_or_qs(page_model_or_qs, info):
    request = info.context
    if inspect.isclass(page_model_or_qs) \
            and issubclass(page_model_or_qs, models.Model):
        qs = page_model_or_qs.objects.all()
    else:
        qs = page_model_or_qs.all()

    qs = exclude_invisible_pages(request, qs)
    qs = qs.select_related('content_type')
    return qs
