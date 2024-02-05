from importlib import reload
import milki_controller
reload (milki_controller)
from milki_controller import MilkiController

import traceback

def main(app_name):
    try:
        m_controller = MilkiController(app_name)
        m_controller.start_view()
        m_controller.setting_items()
    except:
        traceback.print_exc()
