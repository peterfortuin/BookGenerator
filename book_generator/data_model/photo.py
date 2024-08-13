from data_model.element import Element


class Photo(Element):

    def __init__(self, path):
        self.path = path

    def render(self):
        pass
