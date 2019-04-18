from django.utils.translation import ugettext_lazy as _

import graphene

from wagtail_graphql.types import SiteObjectType


class CurrentSiteMixin:
    current_site = graphene.Field(
        SiteObjectType, description=_('Current site information.')
    )

    def resolve_current_site(self, info):
        request = info.context
        return request.site
