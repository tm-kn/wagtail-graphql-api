from django import test

from wagtail.core.models import Site

from graphene_django.views import GraphQLView


class GraphQLQueryTestCaseMixin:
    def graphql_query(self, query):
        rf = test.RequestFactory()
        request = rf.post('/', {
            'query': query
        })
        request.site = Site.objects.first()
        return GraphQLView.as_view()(request)
