import collections

from wagtail.core.models import Page, get_page_models

from wagtail_graphql.models import GraphQLEnabledPage, GraphQLField
from wagtail_graphql.types.pages import create_page_type


class PageInventory:
    """
    Store metadata about Wagtail page models exposed to GraphQL.
    """

    def __init__(self):
        self.__page_models = set()
        self.__page_model_fields = collections.OrderedDict()
        self.__page_graphql_types = collections.OrderedDict()
        self.resolve_page_models()

    @property
    def page_models(self):
        return (model for model in self.__page_models)

    def get_page_model_fields_for(self, model):
        return tuple(self.__page_model_fields[model])

    @property
    def page_graphql_types(self):
        return self.__page_graphql_types.items()

    def resolve_page_models(self):
        """
        Find all Wagtail page models eligible to be in the GraphQL
        endpoint.
        """
        for model in get_page_models():
            # Check if the page model is GraphQL enabled
            if issubclass(model, GraphQLEnabledPage) or model is Page:
                self.__page_models.add(model)
                self.resolve_page_model_fields(model)

        self.resolve_page_graphql_types()

    def resolve_page_model_fields(self, model):
        """
        Find all GraphQL field definitions set on the registered
        models.
        """
        assert model not in self.__page_model_fields, (
            f"{model}'s fields have been already registered.")

        raw_fields = tuple(getattr(model, 'graphql_fields', tuple()))

        fields = collections.OrderedDict()

        for raw_field in raw_fields:
            if not isinstance(raw_field, GraphQLField):
                raise ValueError('Field must be a GraphQLField instance, not '
                                 f'{type(raw_field)}')
            assert raw_field.name not in fields, (
                f'{raw_field.name} for {model} is duplicated.')

            fields[raw_field.name] = raw_field

        self.__page_model_fields[model] = list(fields.values())

    def resolve_page_graphql_types(self):
        """
        Convert page models and field definitions into GraphQL types.
        """
        for page_model in self.page_models:
            graphql_type = create_page_type(
                page_model, self.get_page_model_fields_for(page_model))
            assert page_model not in self.__page_graphql_types, (
                f'{page_model} has already been converted to a GraphQL object')
            self.__page_graphql_types[page_model] = graphql_type
