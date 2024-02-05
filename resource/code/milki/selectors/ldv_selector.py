import selector
# reload (selector)
from selector import Selector

class LdvSelector(Selector):
    _items = None
    def __init__(self):
        Selector.__init__(self)
        self.set_title("LDV Option")
        self._items = []
        # self._items.append(["List", 'Export Order', ['maya', 'fbx']] )
        # self._items.append(["CheckBox", 'Publish Anim Shader', ["Is Anim Shader"]])
        self._items.append(["CheckBox", 'Arnold Attribute of GEOShape', ["Export Attribute"]])
        self._items.append(["CheckBox", 'Bake TX', ["Export Tx"]])
        self._items.append(["CheckBox", 'Pub & Copy Texture file', ["Export Texture"]])
        # self._items.append(["Milki_Edit", 'Create Variation', [""]])
        self._items.append(["edit", 'Create Variation', [""]])


    def get_items(self):
        return self._items
