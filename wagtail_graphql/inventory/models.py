from django.db.models import Model as DjangoModel

from wagtail.core.models import Page
from wagtail.snippets.models import get_snippet_models

from wagtail_graphql import GraphQLEnabledModel
from wagtail_graphql.inventory.base import BaseModelInventory
from wagtail_graphql.types.base import create_model_type


class ModelInventory(BaseModelInventory):
    """
    Inventory of models that are not pages nor snippets.
    """

    def create_model_graphql_type(self, model, fields):
        return create_model_type(model, fields)

    def resolve_models(self):
        """
        Resolve registered Django models omitting pages and snippets. The
        models need to subclass
        :class:`wagtail_graphql.models.GraphQLEnabledModel`.
        """

        snippets = get_snippet_models()

        for model in GraphQLEnabledModel.__subclasses__():
            # Do allow Django models only.
            if not issubclass(model, DjangoModel):
                raise TypeError('Only Django models are supported')

            # Do not register pages
            if issubclass(model, Page):
                continue

            # Do not register snippets.
            if model in snippets:
                continue

            # Do not allow registering abstract models.
            if model._meta.abstract:
                raise TypeError('Cannot register abstract models')

            self._models.add(model)
            self.resolve_model_fields_for(model)
