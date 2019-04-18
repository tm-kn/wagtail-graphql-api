from wagtail.core.models import Site

import graphene
import graphene_django


class SiteObjectType(graphene_django.DjangoObjectType):
    name = graphene.String()

    class Meta:
        model = Site
        only_fields = ('id', 'name')

    def resolve_name(self, info):
        return self.site_name
