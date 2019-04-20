import django.conf

#: Specify default Wagtail's image rendition filter used by the API
#: if not specified explicitly.
WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER = getattr(
    django.conf.settings, 'WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER',
    'original'
)

#: Specify a list of allowed image rendition filters that can be used in the
#: API. Use ``['*']`` to disable the check.
WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS = getattr(
    django.conf.settings, 'WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS',
    ('fill-200x200', 'width-2000')
)

#: If search query is used in the API, a hit can be added to the Wagtail
#: search Query object by setting this to ``True``.
WAGTAIL_GRAPHQL_ADD_SEARCH_HIT = getattr(
    django.conf.settings, 'WAGTAIL_GRAPHQL_ADD_SEARCH_HIT', False
)

#: Enable images list in the GraphQL schema.
WAGTAIL_GRAPHQL_ENABLE_IMAGES = getattr(
    django.conf.settings, 'WAGTAIL_GRAPHQL_ENABLE_IMAGES', True
)

#: Enable documents list in the GraphQL schema.
WAGTAIL_GRAPHQL_ENABLE_DOCUMENTS = getattr(
    django.conf.settings, 'WAGTAIL_GRAPHQL_ENABLE_DOCUMENTS', True
)
