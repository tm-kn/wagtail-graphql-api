import inspect

from django.utils.translation import ugettext_lazy as _

from wagtail.search.index import class_is_indexed

import graphene
import graphene_django

from wagtail_graphql.types.scalars import PositiveInt


class QuerySetList(graphene.List):
    def __init__(self, of_type, *args, **kwargs):
        enable_limit = kwargs.pop('enable_limit', True)
        enable_offset = kwargs.pop('enable_offset', True)
        enable_search = kwargs.pop('enable_search', True)

        # Check if the type is a Django model type. Do not perform the
        # check if value is lazy.
        if inspect.isclass(of_type) and not issubclass(
            of_type, graphene_django.DjangoObjectType
        ):
            raise TypeError(
                f'{of_type} is not a subclass of DjangoObjectType and it '
                'cannot be used with QuerySetList.'
            )
        # Enable limiting on the queryset.
        if enable_limit is True and 'limit' not in kwargs:
            kwargs['limit'] = graphene.Argument(
                PositiveInt,
                description=_('Limit a number of resulting objects.')
            )

        # Enable offset on the queryset.
        if enable_offset is True and 'offset' not in kwargs:
            kwargs['offset'] = graphene.Argument(
                PositiveInt,
                description=_(
                    'Number of records skipped from the beginning of the '
                    'results set.'
                )
            )

        # If type is provided as a lazy value (e.g. using lambda), then
        # the search has to be enabled explicitly.
        if (
            (enable_search is True and not inspect.isclass(of_type))
            or (enable_search is True and inspect.isclass(of_type)
                and class_is_indexed(of_type._meta.model)
                and 'search_query' not in kwargs)
        ):
            kwargs['search_query'] = graphene.Argument(
                graphene.String,
                description=_('Filter the results using Wagtail\'s search.')
            )

        if 'id' not in kwargs:
            kwargs['id'] = graphene.Argument(
                graphene.ID,
                description=_('Filter by ID'),
            )

        super().__init__(of_type, *args, **kwargs)
