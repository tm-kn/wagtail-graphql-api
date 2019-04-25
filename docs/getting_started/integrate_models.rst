Integrate models
================

By default the library will only add a GraphQL pages endpoint for the
`wagtail's core Page model
<https://docs.wagtail.io/en/stable/reference/pages/model_reference.html#page>`_.
It can be queried via the GraphQL endpoint with the following query:

.. code::

   query {
     pages {
       wagtailcore {
          page {
            id
            title
            url
          }
       }
     }
   }

Enabling page model to be accessible via GraphQL endpoint
---------------------------------------------------------
To query any specific page model fields, it needs to first be registered. To do
that the page model has to inherit
:class:`wagtail_graphql.models.GraphQLEnabledModel`.

.. code-block:: python
   :emphasize-lines: 8

   # blog/models.py
   from wagtail.core.fields import StreamField
   from wagtail.core.models import Page

   from wagtail_graphql.models import GraphQLEnabledModel


   class BlogPage(GraphQLEnabledModel, Page):
       introduction = models.TextField(help_text='Text to describe the page',
                                       blank=True)
       body = StreamField(BaseStreamBlock(), verbose_name="Page body", blank=True)

Assuming that the model exists under the ``blog`` app, it should be possible to
query it with the following query:


.. code::

   query {
     pages {
       blog {
         blogPage {
           id
           title
           url
         }
       }
     }
   }

Specifying GraphQL fields
-------------------------

The fields exposed in the endpoint will also have to be explicitly defined. It
requires adding ``graphql_fields`` list with
:class:`wagtail_graphql.models.GraphQLField` instances to the model definition,
e.g.

.. code-block:: python
   :emphasize-lines: 13-16

   # blog/models.py
   from wagtail.core.fields import StreamField
   from wagtail.core.models import Page

   from wagtail_graphql.models import GraphQLEnabledModel, GraphQLField


   class BlogPage(GraphQLEnabledModel, Page):
       introduction = models.TextField(help_text='Text to describe the page',
                                       blank=True)
       body = StreamField(BaseStreamBlock(), verbose_name="Page body", blank=True)

       graphql_fields = [
           GraphQLField('introduction'),
           GraphQLField('body'),
       ]

Now those fields should be accessible via the endpoint in the following way:

.. code::

   query {
     pages {
       blog {
         blogPage {
           introduction
           body
         }
       }
     }
   }

Snippets
--------

Snippets that inherit :class:`wagtail_graphql.models.GraphQLEnabledModel` will
be accessible via the GraphQL endpoint. The query structure is as follows:

.. code-block::

   query {
     snippets {
       appLabel {
         modelName {
           id
         }
      }
     }
   }

Custom models
-------------

Custom models object types can also be added to the GraphQL schema with this
library in the same way as page models or snippets.
The only difference to the snippets and pages is that that it will
not be query-able. The sole point will be to register the object type in the
schema so it can be used to resolve related objects or can be used as a custom
field types without having to manually specify the Graphene type.
