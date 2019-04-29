wagtail-graphql-api
===================

GraphQL module for the `Wagtail CMS <https://wagtail.io/>`_. It is based on
the `Graphene framework <https://graphene-python.org/>`_.

Documentation
~~~~~~~~~~~~~

Set up a virtual environment.

.. code:: sh

   python3 -m venv venv
   source venv/bin/activate

In the project root, install the package.

.. code:: sh

   flit install --symlink --python $(which python) --extra all

Go to the ``docs`` folder and generate the documentation

.. code:: sh

   make html

You can serve the documentation from the web server.

.. code:: sh

   python -m http.server -d _build/html/ 9000

The documentation will be accessible at http://localhost:9000.
