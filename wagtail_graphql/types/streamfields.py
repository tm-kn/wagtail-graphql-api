from wagtail.core.blocks import StreamValue

import graphene


class StreamField(graphene.JSONString):
    """
    Scalar used to represent a Wagtail's StreamField value.
    """

    @staticmethod
    def serialize(value):
        if not isinstance(value, StreamValue):
            raise ValueError('StreamField can only serialize StreamValue.')

        # Currently just return the raw JSON data from the database.
        return value.stream_data
