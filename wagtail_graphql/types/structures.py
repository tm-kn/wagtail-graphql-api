from wagtail.search import index

import graphene
import graphene_django

from wagtail_graphql.types.scalars import PositiveInt


class QuerySetList(graphene.List):
    def __init__(self, of_type, *args, **kwargs):
        if not issubclass(of_type, graphene_django.DjangoObjectType):
            raise TypeError(
                f'{of_type} is not a subclass of DjangoObjectType and it '
                'cannot be used with QuerySetList.'
            )

        if 'limit' not in kwargs:
            kwargs['limit'] = PositiveInt()

        if 'order' not in kwargs:
            kwargs['order'] = PositiveInt()

        if (
            issubclass(of_type._meta.model, index.Indexed)
            and 'search_query' not in kwargs
        ):
            kwargs['search_query'] = graphene.String()

        super().__init__(of_type, *args, **kwargs)
