import django.conf

WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER = getattr(
    django.conf.settings, 'WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER',
    'original'
)

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
