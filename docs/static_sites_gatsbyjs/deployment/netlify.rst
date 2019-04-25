Netlify
=======

`Netlify <https://www.netlify.com/>`_ is a platform that allows deployment of
static sites.

#. Import your website from Git.
#. In the app settings, go to *Buid & Deploy* and *Environment*.
#. Add an environment variable ``WAGTAIL_GRAPHQL_ENDPOINT`` pointing at your
   website's GraphQL endpoint.
#. Trigger the build.

For more information consult `GatsbyJS's guide
<https://www.gatsbyjs.org/docs/hosting-on-netlify/>`_.


Automatic deployments from Wagtail
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Netlify allows creating build hooks. They are URLs that can be used to trigger
a new deployment.

To set up a deployment hook on page publish in Wagtail, please add a new signal
handler in the project.

.. code:: python

   # models.py
   from django.conf import settings

   from wagtail.core.signals import page_published, page_unpublished

   import requests


   def deploy_to_netlify_on_change(**kwargs):
       try:
          netlify_deploy_hook_url = getattr(settings, 'NETLIFY_DEPLOY_HOOK_URL')
       except KeyError:
          return
       if not netlify_deploy_hook_url:
          return
       r = requests.post(netlify_deploy_hook_url)
       r.raise_for_status()


   page_published.connect(deploy_to_netlify_on_change)
   page_unpublished.connect(deploy_to_netlify_on_change)

Then add the Netlify deploy hook to your settings.

.. code:: python

   # settings.py
   import os

   if 'NETLIFY_DEPLOY_HOOK_URL' in os.environ:
       NETLIFY_DEPLOY_HOOK_URL = os.environ['NETLIFY_DEPLOY_HOOK_URL']

#. Go to the Netlify app settings, *Build & Deploy* and *Build Hooks*. Add a new
   build hook for the Wagtail CMS.
#. On the back-end server set the environment variable ``NETLIFY_DEPLOY_HOOK_URL``
   to the generated hook URL.
