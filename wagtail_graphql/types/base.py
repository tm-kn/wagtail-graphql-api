import graphene_django


def create_model_type(model, fields, meta_attrs=None):
    new_meta_attrs = {
        'model': model,
        'only_fields': tuple(field.name for field in fields)
        or (model._meta.pk.name, ),
    }
    if meta_attrs is not None:
        new_meta_attrs.update(meta_attrs)

    meta = type('Meta', tuple(), new_meta_attrs)
    return type(
        f'{model.__name__}ObjectType', (graphene_django.DjangoObjectType, ),
        {'Meta': meta}
    )
