import django.conf
from django.test.signals import setting_changed

#: Specify default Wagtail's image rendition filter used by the API
#: if not specified explicitly.
WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER = None

#: Specify a list of allowed image rendition filters that can be used in the
#: API. Use ``['*']`` to disable the check.
WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS = None

#: If search query is used in the API, a hit can be added to the Wagtail
#: search Query object by setting this to ``True``.
WAGTAIL_GRAPHQL_ADD_SEARCH_HIT = None

#: Enable images list in the GraphQL schema.
WAGTAIL_GRAPHQL_ENABLE_IMAGES = None

#: Enable documents list in the GraphQL schema.
WAGTAIL_GRAPHQL_ENABLE_DOCUMENTS = None


def set_settings():
    global WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER
    global WAGTAIL_GRAPHQL_ADD_SEARCH_HIT
    global WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS
    global WAGTAIL_GRAPHQL_ADD_SEARCH_HIT
    global WAGTAIL_GRAPHQL_ENABLE_IMAGES
    global WAGTAIL_GRAPHQL_ENABLE_DOCUMENTS

    WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER = getattr(
        django.conf.settings, 'WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER',
        'original')

    WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS = getattr(
        django.conf.settings, 'WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS',
        ('fill-200x200', 'width-2000')
    )

    WAGTAIL_GRAPHQL_ADD_SEARCH_HIT = getattr(
        django.conf.settings, 'WAGTAIL_GRAPHQL_ADD_SEARCH_HIT', False
    )

    WAGTAIL_GRAPHQL_ENABLE_IMAGES = getattr(
        django.conf.settings, 'WAGTAIL_GRAPHQL_ENABLE_IMAGES', True
    )

    WAGTAIL_GRAPHQL_ENABLE_DOCUMENTS = getattr(
        django.conf.settings, 'WAGTAIL_GRAPHQL_ENABLE_DOCUMENTS', True
    )


# Set default settings
set_settings()


def reload_settings(**kwargs):
    setting = kwargs['setting']
    if setting.startswith('WAGTAIL_GRAPHQL_'):
        set_settings()


# Reload settings when they change during unit testing.
setting_changed.connect(reload_settings)
