class Page:
    def __init__(self, *elements):
        self.elements = elements

    def add_element(self, element):
        self.elements.append(element)

    def render(self):
        for element in self.elements:
            element.render()
