from wagtail.core.models import Page, get_page_models

from wagtail_graphql.inventory.base import ModelInventory
from wagtail_graphql.models import GraphQLEnabledPage
from wagtail_graphql.types import create_page_type


class PageInventory(ModelInventory):
    """
    Store metadata about Wagtail page models exposed to GraphQL.
    """

    def resolve_models(self):
        """
        Find all Wagtail page models eligible to be in the GraphQL
        endpoint.
        """
        for model in get_page_models():
            assert model not in self._models
            # Check if the page model is GraphQL enabled
            if issubclass(model, GraphQLEnabledPage) or model is Page:
                self._models.add(model)
                self.resolve_model_fields_for(model)

    def create_model_graphql_type(self, model, fields):
        return create_page_type(model, fields)
