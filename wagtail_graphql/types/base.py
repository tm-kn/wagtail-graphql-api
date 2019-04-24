from django.utils.translation import ugettext_lazy as _

from wagtail.core.fields import StreamField

import graphene_django

from wagtail_graphql.types.streamfields import StreamFieldSerializer


def create_model_type(model, fields, meta_attrs=None):
    """
    Create a generic GraphQL type for a Django model.

    :param model: Django model.
    :param fields: A list of :class:`wagtail_graphql.models.GraphQLField`
                   instances to be used on the type.
    :param meta_attrs: Additional meta attributes to be passed to the new
                       GraphQL object type.
    """
    attrs = {}

    new_meta_attrs = {
        'model': model,
        'only_fields': (
            tuple(field.name for field in fields) or (model._meta.pk.name, )
        ),
        'description': (
            _('Auto-generated GraphQL type for the "%s" model of app "%s".') %
            (model.__name__, model._meta.app_label)
        ),
    }
    if meta_attrs is not None:
        new_meta_attrs.update(meta_attrs)

    # Set custom field types and resolve functions
    for field in fields:
        if field.graphql_type is not None:
            attrs[field.name] = field.graphql_type

        if field.resolve_func is not None:
            attrs[f'resolve_{field.name}'] = field.resolve_func
        else:
            # Set a custom resolve function for stream fields
            if isinstance(model._meta.get_field(field.name), StreamField):

                def resolve_stream_field(name):
                    def inner(self, info, **kwargs):
                        init_kwargs = {
                            'request': info.context,
                            'absolute_urls': kwargs.get('absolute', True),
                        }
                        serializer = StreamFieldSerializer(**init_kwargs)
                        return serializer.serialize(getattr(self, name))

                    return inner

                attrs[f'resolve_{field.name}'] = resolve_stream_field(
                    field.name
                )

    meta = type('Meta', tuple(), new_meta_attrs)
    attrs['Meta'] = meta

    return type(
        f'{model._meta.app_label.capitalize()}{model.__name__}ObjectType',
        (graphene_django.DjangoObjectType, ), attrs
    )
