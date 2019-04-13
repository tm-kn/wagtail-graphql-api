from wagtail.core.models import get_page_models


class Inventory:
    def __init__(self):
        self.resolve_pages()

    def resolve_pages(self):
        self.__page_models = get_page_models()

    @property
    def page_models(self):
        return (model for model in self.__page_models)


inventory = Inventory()
