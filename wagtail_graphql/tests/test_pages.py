from django import test

from graphene_django.views import GraphQLView


class TestGraphQLPages(test.TestCase):
    def setUp(self):
        self.request_factory = test.RequestFactory()

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
        request = self.request_factory.post('/', {
            'query': query
        })
        response = GraphQLView.as_view()(request)
        self.assertEqual(response.status_code, 200)
