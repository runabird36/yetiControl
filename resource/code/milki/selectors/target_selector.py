import selector
# reload (selector)
from selector import Selector
import socket


from general_md_3x import LUCY




class TargetSelector(Selector):
    _items = None
    def __init__(self, ):
        Selector.__init__(self)
        self.set_title("Select Target")
        self._items = []



    def set_items(self, targets):

        real_targets = []
        for _tar in targets:
            if '|' in _tar:
                real_tar = _tar.split('|')[-1]
            else:
                real_tar = _tar
            real_targets.append(real_tar)
        real_targets = list(set(real_targets))
        self.set_items_list_with_targets(real_targets)

    def get_items(self):
        return self._items

    def set_items_list_with_targets(self, targets):
        self._items.append(["List", "export targets", targets])
        if LUCY.get_category() == 'sequence':
            self._items.append(["Button", "plus button", ['']])
