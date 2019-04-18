from django.utils.translation import ugettext_lazy as _

import graphene_django


def create_model_type(model, fields, meta_attrs=None):
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

    meta = type('Meta', tuple(), new_meta_attrs)

    return type(
        f'{model._meta.app_label.capitalize()}{model.__name__}ObjectType',
        (graphene_django.DjangoObjectType, ), {'Meta': meta}
    )
