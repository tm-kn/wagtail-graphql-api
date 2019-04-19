from wagtail.core.blocks import StreamValue

import graphene


class StreamField(graphene.JSONString):
    @staticmethod
    def serialize(value):
        if not isinstance(value, StreamValue):
            raise ValueError('StreamField can only serialize StreamValue.')
        return value.stream_data
