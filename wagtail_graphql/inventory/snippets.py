from wagtail.snippets.models import get_snippet_models

from wagtail_graphql.inventory.base import ModelInventory
from wagtail_graphql.models import GraphQLEnabledModel


class SnippetInventory(ModelInventory):
    def resolve_models(self):
        for snippet_model in get_snippet_models():
            if not isinstance(snippet_model, GraphQLEnabledModel):
                continue
            self._models.append(snippet_model)
            self.resolve_model_fields_for(snippet_model)

    def create_model_graphql_type(self, model, fields):
        raise NotImplementedError
