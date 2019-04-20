from graphene.types import Int


class PositiveInt(Int):
    """
    GraphQL type for an integer that must be equal or greater than zero.
    """

    @staticmethod
    def parse_literal(node):
        return_value = Int.parse_literal(node)
        if return_value is not None:
            if return_value >= 0:
                return return_value
