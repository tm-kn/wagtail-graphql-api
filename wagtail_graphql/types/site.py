from wagtail.core.models import Site

import graphene
import graphene_django


class SiteObjectType(graphene_django.DjangoObjectType):
    """
    GraphQL representation of the Wagtail's Site model.
    """

    name = graphene.String()

    class Meta:
        model = Site
        only_fields = ('id', 'name')

    def resolve_name(self, info):
        """
        Map ``Site.site_name`` to :attr:`name` for convenience.
        """
        return self.site_name
