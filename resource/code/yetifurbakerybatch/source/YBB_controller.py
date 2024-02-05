


import YBB_path_module
from view.YBB_bake_dialog import MainWindow


class YetiFurBakery():
    def __init__(self) -> None:
        self.ui = MainWindow()


    def run(self) -> None:
        self.ui.show()



if __name__ == "__main__":
    engine = YetiFurBakery()
    engine.run()