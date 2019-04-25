Static sites generation with GatsbyJS
=====================================

This guide will guide developers towards developing a statically-generated site
with GatsbyJS.

.. note::

   This section requires the reader to be familiar with technologies such as:

     * `React <https://reactjs.org/>`_
     * `GatsbyJS <https://www.gatsbyjs.org/>`_
     * JavaScript language (EcmaScript 6)

GatsbyJS is a static site generator that can be used together with an external
GraphQL source, such as a Wagtail GraphQL API generated with this library.

Requirements
~~~~~~~~~~~~

* `Node.js <https://nodejs.org/en/download/>`_ (recommended newest LTS version)
* Gatsby CLI installed (`NPM <https://www.npmjs.com/package/gatsby-cli>`_)
* A Wagtail project with the GraphQL API enabled using this library.

New GatsbyJS project
~~~~~~~~~~~~~~~~~~~~

.. note::

   This guide will use ``npm`` commands, but equivalent ``yarn`` commands can
   be used as well.

To aid the basic set-up, a template for a new Gatsby project to use with this
library can be used to bootstrap a new project using the following command:

.. code:: sh

   gatsby new your-project-name https://github.com/tm-kn/wagtail-graphql-api-gatsby-starter
   cd your-project-name

.. note::

   The template assumes that you use a default Wagtail start project. If you do
   not, please comment out
   ``'home.HomePage': path.resolve('src', 'pages', 'home-page.js')`` in
   ``gatsby-node.js``.

Before generating the site, the Django server must be started (``./manage.py
runserver`` in the Wagtail's project directory). Next step is to point at the
server location using an environment variable or ``.env`` file. It should be
sufficient to copy ``.env.example`` to ``.env`` (``cp .env.example .env``). The
contents of ``.env`` need to show the path to the GraphQL endpoint, e.g.

.. code:: sh

   WAGTAIL_GRAPHQL_ENDPOINT=http://localhost:8000/graphql/

Then the Gatsby development server can be started by executing ``npm start``.
After the server started, the command line should output a link which can be
used to access the website (by default http://localhost:9000/).

.. toctree::
   :maxdepth: 1
   :hidden:

   custom_page_types
