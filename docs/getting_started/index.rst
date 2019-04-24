Getting started
===============


.. toctree::
   :caption: Contents:

Requirements
~~~~~~~~~~~~

* `Python 3 <https://www.python.org/downloads/>`_
* A `Wagtail project <https://wagtail.io/developers/>`_

If you do not have a Wagtail project set up, please follow the
`guide <http://docs.wagtail.io/en/stable/getting_started/tutorial.html>`_
to create one.

Download
~~~~~~~~

.. _PyPI: https://pypi.org/project/wagtail-graphql-api

This package can be installed from the PyPI_ via pip.

.. code:: sh

   pip install wagtail-graphql-api

This package should be installed as a dependency of an existing Wagtail
project.

Configuration
~~~~~~~~~~~~~

The package is a Django application. It needs to be added to your Wagtail
project's setting file. Also ``graphene_django`` is a package used by
``wagtail-graphql-api``, therefore it needs to be enabled as well.

.. code:: python

   # settings.py

   INSTALLED_APPS = [
      # The rest of your apps...
      'graphene_django',
      'wagtail_graphql',
   ]

Next step is to set up `Graphene <https://graphene-python.org/>`_ to use the
schema provided by ``wagtail-graphql-api``.

.. code:: python

   # settings.py

   GRAPHENE = {
      'SCHEMA': 'wagtail_graphql.schema.schema'
   }

After that is done, the GraphQL endpoint has to be exposed in the URL
dispatcher. To do that you need to add a path in the configuration, usually it
is a `urls.py` file.

.. code:: python

   # urls.py

   from django.urls import path

   from graphene_django.views import GraphQLView

   urlpatterns = [
      # Other URL paths...
      path('graphql/', GraphQLView.as_view(graphiql=True, pretty=True)),
      # Other URL paths...
   ]

Then after the development server is started (``./manage.py runserver``), the
GraphQL endpoint should be accessible via http://localhost:8000/graphql/.
