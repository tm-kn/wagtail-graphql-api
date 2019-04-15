import collections

from wagtail_graphql.models import GraphQLField


class ModelInventory:
    def __init__(self):
        self._models = set()
        self._model_fields = collections.OrderedDict()
        self._graphql_types = collections.OrderedDict()
        self.resolve_models()
        self.resolve_graphql_types()

    def create_model_graphql_type(self, model, fields):
        raise NotImplementedError

    def resolve_models(self):
        raise NotImplementedError

    @property
    def models(self):
        return (model for model in self._models)

    @property
    def graphql_types(self):
        return self._graphql_types.items()

    def get_model_fields_for(self, model):
        """
        Find all GraphQL field definitions set on the registered
        models.
        """
        return tuple(self._model_fields[model])

    def resolve_model_fields_for(self, model):
        assert model not in self._model_fields, (
            f"{model}'s fields have been already registered."
        )
        raw_fields = tuple(getattr(model, 'graphql_fields', tuple()))

        fields = collections.OrderedDict()

        for raw_field in raw_fields:
            if not isinstance(raw_field, GraphQLField):
                raise ValueError(
                    'Field must be a GraphQLField instance, not '
                    f'{type(raw_field)}'
                )
            assert raw_field.name not in fields, (
                f'{raw_field.name} for {model} is duplicated.'
            )
            fields[raw_field.name] = raw_field

        # Add an ID field if it is not defined.
        if not any(
            f for f in fields.keys() if f in (model._meta.pk.name, 'pk')
        ):
            fields[model._meta.pk.name] = GraphQLField(model._meta.pk.name)

        self._model_fields[model] = tuple(fields.values())

    def resolve_graphql_types(self):
        """
        Convert models and field definitions into GraphQL types.
        """
        for model in self.models:
            assert model not in self._graphql_types, (
                f'{model} has already been converted to a GraphQL object'
            )

            graphql_type = self.create_model_graphql_type(
                model, self.get_model_fields_for(model)
            )
            self._graphql_types[model] = graphql_type
