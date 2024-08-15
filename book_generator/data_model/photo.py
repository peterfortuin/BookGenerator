from urllib.request import urlopen

from data_model.element import Element

from PIL import Image


class Photo(Element):

    def __init__(self, path):
        self.path = path

        if self.path.startswith(("http://", "https://")):
            self.image = Image.open(urlopen(self.path))
        else:
            self.image = Image.open(path)
