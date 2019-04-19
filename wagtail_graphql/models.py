class GraphQLEnabledModel:
    pass


class GraphQLField:
    def __init__(self, name, resolve_func=None, graphql_type=None):
        if not isinstance(name, str):
            raise TypeError('Name has to be a string')
        name = name.strip()
        if not name:
            raise ValueError('Field name cannot be empty')
        self.__name = name
        self.__resolve_func = resolve_func
        self.__graphql_type = graphql_type

    @property
    def name(self):
        return self.__name

    @property
    def resolve_func(self):
        return self.__resolve_func

    @property
    def graphql_type(self):
        return self.__graphql_type
