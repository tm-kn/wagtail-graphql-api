import json

from django import test

from wagtail_graphql.tests.utils import GraphQLQueryTestCaseMixin


class TestImages(GraphQLQueryTestCaseMixin, test.TestCase):
    def test_images_endpoint_returns_200(self):
        response = self.graphql_query(
            """{
            images {
                id
            }
        }"""
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('errors', json.loads(response.content))

    @test.override_settings(WAGTAIL_GRAPHQL_ENABLE_IMAGES=False)
    def test_images_endpoint_fails_if_disabled(self):
        response = self.graphql_query(
            """{
            images {
                id
            }
        }"""
        )

        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.content)
        self.assertIn('errors', response_json)
        self.assertIsNone(response_json['data']['images'])
        self.assertEqual(
            response_json['errors'][0]['message'],
            'Images endpoint is disabled.'
        )
        self.assertEqual(response_json['errors'][0]['path'], ['images'])
