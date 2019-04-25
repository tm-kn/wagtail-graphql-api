Custom page types
=================

Background
~~~~~~~~~~

The GraphQL query used to generate a website structure is placed in
the ``gatsby-node.js`` file within the ``createPages`` function:

.. code:: javascript

   const path = require('path');

   const PAGE_TYPES = {
      'home.HomePage': path.resolve('src', 'pages', 'home-page.js')
   };

   function getComponentPathForType (pageType) {
      return PAGE_TYPES[pageType] || path.resolve('src', 'pages', 'base-page.js');
   }

   exports.createPages = ({ graphql, actions }) => {
      const { createPage } = actions;

      return graphql(` {
            wagtail {
               pages {
                  wagtailcore {
                     page {
                        id
                        url
                        pageType
                     }
                  }
               }
            }
         }
      `).then(({ data, errors }) => {
         if (errors) {
            throw errors;
         }

         data.wagtail.pages.wagtailcore.page.forEach(({ url, id, pageType }) => {
            createPage({
               path: url,
               component: getComponentPathForType(pageType),
               context: {
                  pageID: id
               }
            });
         });
      });
   };

It uses the core Wagtail's Page model to find all the pages and its paths.
Using the ``getComponentPathForType`` function it determines what React
component to use for the given page type. The available types are defined in
the ``PAGE_TYPES`` object. By default the ``base-page.js`` component will be
used for a page type without a specific component mapped to it.

Defining a custom type
~~~~~~~~~~~~~~~~~~~~~~

In this example a ``locations.LocationPage`` model is used.

To define a custom type you need to create a new React component.

.. code:: javascript

   // src/components/pages/location-page.js
   import React from 'react';
   import { graphql } from 'gatsby';

   import Layout from '../components/layout';
   import SEO from '../components/seo';

   const LocationPage = ({ data }) => {
      // Obtain the page object from the query results.
      // "data" containts the result of the query.
      const page = data.wagtail.pages.locations.locationPage[0];

      return <Layout>
         <SEO title={page.seoTitle} description={page.seoDescription} />
         <h1>{page.title}</h1>
         <h1>I AM THE NEW PAGE TYPE</h1>
      </Layout>;
   };


   // The $pageID value is passed from the context defined in gatsby-node.js.
   export const query = graphql`
      query($pageID: ID) {
         wagtail {
            pages {
               locations {
                  locationPage(id: $pageID) {
                     id
                     title
                     seoTitle
                     seoDescription
                  }
               }
            }
         }
      }
   `;

   export default LocationPage;

Then in ``gatsby-node.js`` the page type has to be added:

.. code:: javascript

   // gatsby-node.js
   const PAGE_TYPES = {
      // Other possible page types
      'locations.LocationPage': path.resolve(
         'src', 'pages', 'location-page.js'
      )
   }

Make sure that the key of the object matches ``pageType`` value of the GraphQL
page object (it is case sensitive).

After that the Gatsby server has to be restarted and the new component should
be used for instances of the new page type.
