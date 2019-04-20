from wagtail.snippets.models import get_snippet_models

from wagtail_graphql.inventory.base import BaseModelInventory
from wagtail_graphql.models import GraphQLEnabledModel
from wagtail_graphql.types.snippets import create_snippet_type


class SnippetInventory(BaseModelInventory):
    """
    Inventory of snippet models.
    """

    def resolve_models(self):
        for model in get_snippet_models():
            if not issubclass(model, GraphQLEnabledModel):
                continue
            self._models.add(model)
            self.resolve_model_fields_for(model)

    def create_model_graphql_type(self, model, fields):
        return create_snippet_type(model, fields)
