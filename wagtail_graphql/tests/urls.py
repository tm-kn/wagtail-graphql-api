from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.images import urls as wagtailimages_urls

from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('images/', include(wagtailimages_urls)),
    path(
        'graphql/',
        csrf_exempt(GraphQLView.as_view(graphiql=True, pretty=True)),
        name='graphql'
    ),
    path('', include(wagtail_urls)),
]
