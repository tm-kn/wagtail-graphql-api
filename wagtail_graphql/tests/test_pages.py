import json

from django import test

from wagtail_graphql.tests.utils import GraphQLQueryTestCaseMixin


class TestGraphQLPages(GraphQLQueryTestCaseMixin, test.TestCase):
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
        response = self.graphql_query(query)
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
        response = self.graphql_query(query)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('errors', json.loads(response.content))
