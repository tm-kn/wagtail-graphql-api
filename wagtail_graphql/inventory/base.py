from wagtail_graphql.inventory.pages import PageInventory


class Inventory:
    """
    Store metadata about objects exposed to the GraphQL endpoints.
    """

    def __init__(self):
        self.__page_inventory = PageInventory()

    @property
    def pages(self):
        return self.__page_inventory
