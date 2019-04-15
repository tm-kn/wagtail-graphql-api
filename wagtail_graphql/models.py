class GraphQLEnabledModel:
    pass


class GraphQLEnabledPage(GraphQLEnabledModel):
    pass


class GraphQLField:
    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError('Name has to be a string')
        name = name.strip()
        if not name:
            raise ValueError('Field name cannot be empty')
        self.__name = name

    @property
    def name(self):
        return self.__name
