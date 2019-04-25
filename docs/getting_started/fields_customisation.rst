Fields customisation
====================

To add a non-database field to the GraphQL object representation of a model, a
special arguments have to be specified on a
:class:`wagtail_graphql.models.GraphQLField` instance.


.. autoclass:: wagtail_graphql.models.GraphQLField
    :show-inheritance:
    :noindex:

The name of the field can be custom as long as it does not interfere with other
field names on the object.

The custom GraphQL type returned by the field can be specified using
``graphql_type`` parameter, e.g.

.. code:: python

   from wagtail_graphql.models import GraphQLField

   GraphQLField('settings', graphql_type=graphene.JSONString)

However if there is no corresponding database field of that name, the field
will not be accessible. To allow that ``resolve_func`` must be specified. The
argument must be a `Graphene-compatible resolver
<https://docs.graphene-python.org/en/latest/types/objecttypes/#resolvers>`_.

.. code:: python

   import json

   import graphene
   from wagtail_graphql.models import GraphQLField

   GraphQLField('settings', graphql_type=graphene.Field(graphene.JSONString)),
                resolve_func=lambda self, info: json.loads(
                    self.settings
                ))


Model object types
------------------

Sometimes it may be necessary to use a Django model as an object type for a
custom non-database field. To refer to an automatically generated object a
special utility function has to be used that will resolve the object type
lazily - :func:`wagtail_graphql.lazy_model_type`.

.. code-block:: python
   :emphasize-lines: 18

    # locations/models.py
    from django.db import models

    from wagtail_graphql import lazy_model_type
    from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField


    class Country(GraphQLEnabledModel, models.Model):
        # Fields about a country


    class LocationPage(GraphQLEnabledModel, Page):
        lat_long = models.CharField()

        graphql_fields = [
            GraphQLField('country',
                        graphql_type=graphene.Field(
                            lazy_model_type('locations.Country')
                        ),
                        resolve_func=lambda self, info: self.get_country()),
        ]

        def get_country(self):
            # Logic to get a country object based on latitude and longitude.
            return country


QuerySetList
------------

:class:`wagtail_graphql.types.structures.QuerySetList` is a custom list type
that adds Django's QuerySet arguments like filtering or ordering. However to
specify it on the model classes it is necessary to import it lazily using
:func:`wagtail_graphql.lazy_queryset_list`. To benefit from the arguments
built-in in the ``QuerySetList``, the queryset has to be filtered through
:func:`wagtail_graphql.utils.get_base_queryset_for_model_or_qs` or if it is a
page :func:`wagtail_graphql.utils.get_base_queryset_for_page_model_or_qs` must
be used.


.. code-block:: python
   :emphasize-lines: 21

    # locations/models.py
    from django.db import models

    from wagtail_graphql import lazy_queryset_list
    from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField


    def resolve_locations(self, info, **kwargs):
        from wagtail_graphql.utils import get_base_queryset_for_page_model_or_qs

        return get_base_queryset_for_page_model_or_qs(
            self.get_location_pages(), info, **kwargs
        )


    class Country(GraphQLEnabledModel, models.Model):
        # Fields about a country

        graphql_fields = [
            GraphQLField('locations', graphql_type=graphene.Field(
                lazy_queryset_list('locations.LocationPage')
            ), resolve_func=resolve_locations)
        ]

        def get_location_pages(self):
            location_pages_queryset = LocationPage.objects.all()
            # Filter the queryset
            return location_pages_queryset


    class LocationPage(GraphQLEnabledModel, Page):
        # Fields about a location
