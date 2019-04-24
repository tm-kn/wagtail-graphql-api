import collections

from wagtail.core.blocks import BoundBlock, ListBlock, StreamValue
from wagtail.core.blocks.struct_block import StructValue
from wagtail.core.rich_text import RichText
from wagtail.documents.models import get_document_model
from wagtail.embeds.blocks import EmbedValue
from wagtail.embeds.embeds import get_embed
from wagtail.images import get_image_model

import graphene

from wagtail_graphql.utils import resolve_absolute_url


def convert_rich_text(source, request, absolute):
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return str(RichText(source))

    soup = BeautifulSoup(source, 'html5lib')

    # Make document links absolute.
    for anchor in soup.find_all('a'):
        if anchor.attrs.get('linktype', '') == 'document':
            try:
                doc = get_document_model().objects.get(pk=anchor.attrs['id'])
                new_tag = soup.new_tag(
                    'a',
                    href=resolve_absolute_url(
                        doc.url, request, absolute=absolute
                    )
                )
                new_tag.append(*anchor.contents)
                anchor.replace_with(new_tag)
            except get_document_model().DoesNotExist:
                new_tag = soup.new_tag('a')
                new_tag.append(*anchor.contents)
                anchor.replace_with(new_tag)

    return str(RichText(str(soup)))


class StreamFieldSerializer:
    def __init__(
        self, request=None, absolute_urls=None, rendition_filter='width-1200'
    ):
        self.request = request
        self.absolute_urls = absolute_urls
        self.rendition_filter = rendition_filter

    def serialize(self, block):
        if isinstance(block, StreamValue):
            return tuple(self.serialize_stream_block(block))
        if isinstance(block, BoundBlock):
            return self.serialize_bound_block(block)

    def serialize_bound_block(self, block):
        return {
            'type': block.block.name,
            'value': self.serialize_block_value(block.block, block.value),
            'id': block.id
        }

    def serialize_block_value(self, block, value):
        if isinstance(value, str):
            return value

        if isinstance(value, RichText):
            return convert_rich_text(
                value.source, self.request, self.absolute_urls
            )

        if isinstance(value, get_image_model()):
            rendition = value.get_rendition(self.rendition_filter)
            return {
                'id': value.id,
                'url': resolve_absolute_url(
                    rendition.url,
                    self.request,
                    absolute=self.absolute_urls is True
                ),
                'title': value.title,
                'alt': rendition.alt,
            }

        if isinstance(value, StructValue):
            return collections.OrderedDict(self.serialize_struct_block(value))

        if isinstance(value, EmbedValue):
            embed = get_embed(value.url)
            return {
                'id': embed.id,
                'html': embed.html,
                'url': value.url,
            }

        if isinstance(block, ListBlock):
            return tuple(self.serialize_list_block(block, value))

        raise RuntimeError(
            f'Cannot serialize StreamField value of type "{type(value)}"'
        )

    def serialize_struct_block(self, value):
        for block_name, bound_block in value.bound_blocks.items():
            yield block_name, self.serialize_block_value(
                bound_block.block, bound_block.value
            )

    def serialize_stream_block(self, stream_block):
        for block in stream_block:
            yield self.serialize(block)

    def serialize_list_block(self, block, value):
        for child_value in value:
            yield self.serialize_block_value(block.child_block, child_value)


class StreamField(graphene.JSONString):
    """
    Scalar used to represent a Wagtail's StreamField value.
    """

    @staticmethod
    def serialize(value):
        # Already serialized.
        if isinstance(value, (list, dict, tuple)):
            return value

        # StreamField not serialized.
        if not isinstance(value, StreamValue):
            raise ValueError('StreamField can only serialize StreamValue.')

        return StreamFieldSerializer().serialize(value)
