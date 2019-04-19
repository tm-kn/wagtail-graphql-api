import json

from django import test

from wagtail.core.models import Site

from graphene_django.views import GraphQLView


class TestGraphQLPages(test.TestCase):
    def setUp(self):
        self.request_factory = test.RequestFactory()

    def _graphql_query(self, query):
        request = self.request_factory.post('/', {
            'query': query
        })
        request.site = Site.objects.first()
        return GraphQLView.as_view()(request)

    def test_graphql_pages_query_returns_200_ok(self):
        query = """
        query {
            pages{
                wagtailcore {
                    page {
                        id
                    }
                }
            }
        }
        """
        response = self._graphql_query(query)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('errors', json.loads(response.content))

    def test_graphql_home_page_returns_200_ok(self):
        query = """
        query {
            pages{
                home {
                    homePage {
                        id
                    }
                }
            }
        }
        """
        response = self._graphql_query(query)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('errors', json.loads(response.content))
