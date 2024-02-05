import checker
# reload (checker)
from checker import Checker

class TestChecker(Checker):

    def __init__(self):
        Checker.__init__(self)
        self.set_title("TestChecker")

    def execute(self):
        self.add_warnning("Test", "warn message", "error")