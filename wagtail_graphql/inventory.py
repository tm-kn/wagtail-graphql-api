import collections

from wagtail.core.models import get_page_models, Page

from wagtail_graphql.models import GraphQLEnabledPage


class Inventory:
    def __init__(self):
        # Resolve the base page model by default
        self.__page_models = set()
        self.__page_model_fields = collections.OrderedDict()
        self.resolve_pages()

    def resolve_pages(self):
        for model in get_page_models():
            # Check if the page model is GraphQL enabled
            if issubclass(model, GraphQLEnabledPage) or model is Page:
                self.__page_models.add(model)
                self.resolve_page_model_fields(model)

    def resolve_page_model_fields(self, model):
        raw_fields = tuple(getattr(model, 'graphql_fields', tuple()))

        fields = self.__page_model_fields[model] = []

        for raw_field in raw_fields:
            if not isinstance(raw_field, str):
                raise ValueError(
                    f'Field must be a string, not {type(raw_field)}'
                )
            fields.append(raw_field)

    @property
    def page_models(self):
        return (model for model in self.__page_models)

    def get_page_model_fields_for(self, model):
        return tuple(self.__page_model_fields[model])


inventory = Inventory()
