Streamfields definition in GatsbyJS
===================================

Each Wagtail project will have its own definition of stream field blocks.
``wagtail-graphql-api`` does a job of serialising them. However each of the
custom blocks has to be defined in the front-end.

The template comes with a StreamField component included however it needs
configuration before it can be used.

.. code:: jsx

   // src/components/stream-field.js
   import React from 'react';

   import RichText from './rich-text';

   const StreamField = ({ value }) => {
      return (
         <div>
            {value.map(block => {
               // Display a different component based on the block type.
               switch (block.type) {
                  // StreamField can define a 'paragraph_block'.
                  case 'paragraph_block':
                     return <RichText key={block.id}>{block.value}</RichText>;
               }
            })}
         </div>
      );
   };

   export default StreamField;

For any new block type a switch case has to be added, e.g. for an
``ImageChooserBlock`` it could be:

.. code:: jsx

    // src/components/stream-field.js
    switch (block.type) {
      // ...
      // other block types
      // ...
      case 'image_block':
         return <img src={block.value.url} alt={block.value.alt} />;
   }

Then any page that has a StreamField, it can use that component, e.g.

.. code:: jsx

   <StreamField value={page.body} />

