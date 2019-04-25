Images
======

Querying all the images
-----------------------

There is an additional field added to allow querying all the available images.
An example query to get all the images may be:

.. code::

   query {
     images {
       id
       title
       rendition {
         url
         alt
       }
     }
   }

This feature can be disabled with a Django setting
``WAGTAIL_GRAPHQL_ENABLE_IMAGES``.

.. code:: python

   # settings.py
   WAGTAIL_GRAPHQL_ENABLE_IMAGES = False

Renditions
----------

The image object type allows to resolve Wagtail image renditions with different
filters.

.. note::

   Different filters are described in the `Wagtail documentation
   <https://docs.wagtail.io/en/stable/topics/images.html>`_.

To specify a desired rendition filter, a `filter` parameter can be used on the
rendition field, e.g.

.. code::

   query {
     images {
       id
       title
       rendition(filter: "width-1200") {
         url
         alt
       }
     }
   }

The rendition filters allowed to be used have to be specified with a Django
setting, ``WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS``.

.. code:: python

   # settings.py
   WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS = ['original', 'width-1200']

.. warning::

   ``['*']`` value can be used for the
   ``WAGTAIL_GRAPHQL_ALLOWED_RENDITION_FILTERS`` setting to whitelist all valid
   rendition filter specifications. However it is discouraged because an
   attacker may send malicious requests to generate a lot of unnecessary
   renditions that may have serious consequences for the server's performance
   or storage space taken.

The default value if the ``filter`` argument is not specified can be set using
the ``WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER`` setting.

.. code:: python

   # settings.py
   WAGTAIL_GRAPHQL_DEFAULT_RENDITION_FILTER = 'original'
