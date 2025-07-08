
from .audio import *


class State:

    def __init__(self, id):
        self.id = id

    def enter(self):
        pass

    def exit(self):
        pass

    def events(self):
        pass

    def process(self):
        pass

    def render(self):
        pass

    def render_ui(self):
        pass