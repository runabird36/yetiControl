import PySide2.QtCore as QtCore


class Docker():
    supply = None
    items = []
    current_item = None

    def __init__(self):
        print('docker init')

    def docking_items(self, items):
        self.items = []
        self.items = items
        self.current_item = self.items[0]

    def get_current_item(self):
        return self.current_item

    def get_next_item(self):
        idx = self.items.index(self.current_item)
        if len(self.items) == idx+1:
            return
        self.current_item = self.items[idx+1]
        return self.current_item

    def get_titles(self):
        print(self.items)
        titles = [item.get_title() for item in self.items]
        return titles

    def get_len_of_items(self):
        return len(self.items)

    def get_item(self, idx):
        if len(self.items)-1 < idx:
            return
        self.current_item = self.items[idx]
        return self.current_item

    def reset_cur_item(self):
        self.current_item = self.items[0]
