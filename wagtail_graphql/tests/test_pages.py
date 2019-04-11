from django import test
from django.urls import reverse


class TestGraphQLPages(test.TestCase):
    def setUp(self):
        self.client = test.Client()

    def test_graphql_pages_query_returns_200_ok(self):
        query = """
        query {
            pages {
                id
            }
        }
        """
        response = self.client.post(reverse('graphql'), {
            'query': query
        })
        self.assertEqual(response.status_code, 200)
