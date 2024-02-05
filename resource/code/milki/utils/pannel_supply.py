from importlib import reload

class PannelSupply():

    res_tree = None
    res_table = None
    select_panel = None
    export_panel = None


    def get_item_pannel(self, item):
        if item.get_type() == "Checker":
            if item.get_title() in ["Name Check", "Transform History Check",\
                                    "Node Name Check", "Freeze transform Check",\
                                    "UVset Check", "Geo Check"]:
                return self._get_res_table()
            return self._get_res_tree()
        elif item.get_type() == "Selector":
            return self._get_select_panel()
        elif item.get_type() == "Exporter":
            # This part for saturn code
            if item.get_title() == 'Saturn Planet Exporter':
                return self._get_saturn_export_panel()
            return self._get_export_panel()

    def _get_res_tree(self):
        if self.res_tree is None:
            import result_tree
            reload (result_tree)
            self.res_tree = result_tree.ResultTree()

        return self.res_tree

    def _get_res_table(self):
        if self.res_table is None:
            import result_table
            reload(result_table)
            self.res_table = result_table.ResultTable()
        return self.res_table

    def _get_select_panel(self):
        if self.select_panel is None:
            import select_panel
            reload (select_panel)
            self.select_panel = select_panel.SelectPanel()
        self.select_panel.refresh()
        return self.select_panel

    def _get_export_panel(self):
        if self.export_panel is None:
            import export_panel
            reload (export_panel)
            self.export_panel = export_panel.ExportPanel()

        return self.export_panel

    def _get_saturn_export_panel(self):
        if self.export_panel is None:
            import saturn_export_panel
            reload (saturn_export_panel)
            self.export_panel = saturn_export_panel.ExportPanel()

        return self.export_panel
