from wagtail_graphql.inventory.models import ModelInventory
from wagtail_graphql.inventory.pages import PageInventory
from wagtail_graphql.inventory.snippets import SnippetInventory


class Inventory:
    """
    Store metadata about objects exposed to the GraphQL endpoints.
    """
    def __init__(self):
        self.__register_inventory('pages', PageInventory())
        self.__register_inventory('snippets', SnippetInventory())
        self.__register_inventory('models', ModelInventory())

    def __register_inventory(self, name, inventory):
        assert not hasattr(self, name), 'Attribute of this name already exists'
        setattr(self, name, inventory)


inventory = Inventory()
