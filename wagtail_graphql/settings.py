import django.conf

WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER = getattr(
    django.conf.settings, 'WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER',
    'original'
)

WAGTAIL_GRAPHQL_ALLOWED_RENDITIONS = getattr(
    django.conf.settings, 'WAGTAIL_GRAPHQL_ALLOWED_RENDITIONS',
    ('fill-200x200', 'width-2000')
)
