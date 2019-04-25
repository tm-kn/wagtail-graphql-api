Querying
========

Example queries facilitating ``QuerySetList`` parameters may be:

QuerySetList
~~~~~~~~~~~~

Searching
---------

If the model is enabled with the `Wagtail Search
<https://docs.wagtail.io/en/stable/topics/search/>`_, ``searchQuery`` parameter
can be used to pass a search query as an argument:

.. code::

   query {
     pages {
       locations {
         locationPage(searchQuery:"test") {
           id
           title
         }
       }
     }
   }

Get a specific object
---------------------

To get an object of a specific ID, the ID can be passed as an argument to the
``id`` parameter.

.. code::

   query($id: ID) {
     pages {
       locations {
         locationPage(id: $id) {
           id
           title
         }
       }
     }
   }

Limit and offset
----------------

.. code::

   query {
     pages {
       locations {
         locationPage(limit: 5, offset: 2) {
           id
           title
         }
       }
     }
   }


Order by
--------

Order by will feed the string into the QuerySet's `order_by
<https://docs.djangoproject.com/en/stable/ref/models/querysets/#django.db.models.query.QuerySet.order_by>`_
method. Multiple fields can be specified with a comma as a delimiter.

.. code::

   query {
     pages {
       locations {
         locationPageByTitleAscending: locationPage(order:"title") {
           id
           title
         }

         locationPageByTitleDescending: locationPage(order:"-title") {
           id
           title
         }

         locationPageByTitleAndID: locationPage(order:"title,-id") {
           id
           title
         }
       }
     }
   }

Page Interface
~~~~~~~~~~~~~~

:class:`wagtail_graphql.types.pages.PageInterface` defines base model pages and
methods that can be used on any page.

The commonly used Wagtail methods available on any page type are:

* Returning one ``PageInterface`` object:
   * ``parent``
   * ``specific``
* Returning list of ``PageInterface`` instances:
   * ``children``
   * ``siblings``
   * ``nextSiblings``
   * ``previousSiblings``
   * ``descendants``
   * ``ancestors``

Pages query mixin
~~~~~~~~~~~~~~~~

The pages query mixin adds two parameters to the standard ``QuerySetList`` set:

* ``depth``
* ``showInMenus``

This allows to filter pages by depth or whether they are supposed to be shown
in the menu. For example, to get a potential set of pages to be used in the
header navigation, the following query may be used:

.. code::

   query {
     pages {
       wagtailcore {
         page(depth: 3, showInMenus: true) {
           id
           title
           pageType
         }
       }
     }
   }
