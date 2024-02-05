

from general_md_3x import LUCY
from importlib import reload
from re import search
from socket import gethostname

class ItemSupply():
    item_dic = {}
    m_sg_tk = None
    p_dialog = None
    def __init__(self, m_sg_tk, progress_dialog, app_name):
        self.m_sg_tk = m_sg_tk
        self.p_dialog = progress_dialog
        self._IS_SHOT_MDL = False
        self.app_name = app_name


    def get_items(self, part):

        entity = LUCY.get_category()

        if part == 'modeling' and entity =='sequence':
            self._IS_SHOT_MDL = True


        if part == 'modeling' and self._IS_SHOT_MDL == False:
            import target_selector
            from target_selector import TargetSelector

            import name_checker
            # reload(name_checker)
            from name_checker import NameChekcer

            import history_checker
            # reload(history_checker)
            from history_checker import HistoryChekcer

            import freeze_checker
            # reload(freeze_checker)
            from freeze_checker import FreezeChecker


            import freeze_selector
            # reload(freeze_selector)
            from freeze_selector import FreezeSelector

            import uvSet_checker
            reload(uvSet_checker)
            from uvSet_checker import UVsetChecker


            import mdl_selector
            # reload(mdl_selector)
            from mdl_selector import MdlSelector


            # import mdl_exporter     # _02
            # reload(mdl_exporter)    # _02
            # # from mdl_exporter import MdlExporter
            # if gethostname() == "3DCGI-PIP-STY":
            #     import mdl_exporter_03     # _02
            #     reload(mdl_exporter_03)    # _02
            #     from mdl_exporter_03 import MdlExporter
            
            # else:
            #     import mdl_exporter     # _02
            #     reload(mdl_exporter)    # _02
            #     from mdl_exporter import MdlExporter

            import mdl_exporter_03     # _02
            reload(mdl_exporter_03)    # _02
            from mdl_exporter_03 import MdlExporter
            

            

            return [TargetSelector(), FreezeSelector(), HistoryChekcer(), NameChekcer(), FreezeChecker(), UVsetChecker(), MdlSelector(), MdlExporter(self.m_sg_tk, self.p_dialog)]
            

            
            
            


        elif part == "shotsculpt" or (part == 'modeling' and self._IS_SHOT_MDL == True):
            import target_selector
            from target_selector import TargetSelector

            import shotMDL_selector
            reload(shotMDL_selector)
            from shotMDL_selector import ShotMDLSelector

            shot_mdl_option_selector = ShotMDLSelector()
            shot_mdl_option_selector.refresh()
            # shot_mdl_option_selector.set_siganls()
            

            import anim_exporter
            reload (anim_exporter)
            from anim_exporter import AnimExporter

            return [TargetSelector(), shot_mdl_option_selector, AnimExporter(self.m_sg_tk, self.p_dialog)]



        elif part == 'lookdev':
            import target_selector
            from target_selector import TargetSelector

            import geo_checker
            # reload (geo_checker)
            from geo_checker import GeoChecker

            import ldv_selector
            reload (ldv_selector)
            from ldv_selector import LdvSelector


            import node_name_checker
            reload (node_name_checker)
            from node_name_checker import NodeNameChecker

            
            
            import ldv_exporter     # _02
            reload(ldv_exporter)    # _02
            from ldv_exporter import LdvExporter
            

            return [TargetSelector(), LdvSelector(), LdvExporter(self.m_sg_tk, self.p_dialog)]

        elif part == 'rigging':
            import target_selector
            from target_selector import TargetSelector

            # import deformed_checker
            # reload (deformed_checker)
            # from deformed_checker import DeformedChecker

            # import geo_checker
            # reload (geo_checker)
            # from geo_checker import GeoChecker

            import rig_exporter
            reload (rig_exporter)
            from rig_exporter import RigExporter

            return [TargetSelector(), RigExporter(self.m_sg_tk, self.p_dialog)]

        

        elif part in ['cloth'] and entity != 'sequence':
            import target_selector
            from target_selector import TargetSelector

            # import deformed_checker
            # reload (deformed_checker)
            # from deformed_checker import DeformedChecker

            # import geo_checker
            # reload (geo_checker)
            # from geo_checker import GeoChecker

            import rig_exporter
            reload (rig_exporter)
            from rig_exporter import RigExporter


            return [TargetSelector(), RigExporter(self.m_sg_tk, self.p_dialog)]
            # return [TargetSelector(),DeformedChecker(), GeoChecker(), RigExporter(self.m_sg_tk, self.p_dialog)]



        elif part in ['layout', 'animation', 'matchmove', 'previz', 'cloth']:
            import target_selector
            reload(target_selector)
            from target_selector import TargetSelector

            import ani_ns_latest_checker
            reload (ani_ns_latest_checker)
            from ani_ns_latest_checker import ANINsLatestChekcer

            import frame_range_checker
            reload (frame_range_checker)
            from frame_range_checker import FrameRangeChecker
            
            import fps_value_checker
            reload (fps_value_checker)
            from fps_value_checker import FPSChecker


            import anim_selector_v03    # _v02
            reload (anim_selector_v03)  # _v02
            from anim_selector_v03 import AnimSelector
            
            import anim_exporter_v03    # _v02
            reload (anim_exporter_v03)  # _v02
            from anim_exporter_v03 import AnimExporter
            
            ani_option_selector = AnimSelector()
            ani_option_selector.refresh()
            
            # if part in ['matchmove']:
            #     return [TargetSelector(), FrameRangeChecker(self.m_sg_tk), ani_option_selector, AnimExporter(self.m_sg_tk, self.p_dialog)]
            if part == 'animation' and LUCY.get_category() == 'assets':
                import rig_exporter
                # reload (rig_exporter)
                from rig_exporter import RigExporter
                return [TargetSelector(), ani_option_selector, AnimExporter(self.m_sg_tk, self.p_dialog)]
                return [TargetSelector(), RigExporter(self.m_sg_tk, self.p_dialog)]
                # return [TargetSelector(), GeoChecker(), ani_option_selector, AnimExporter(self.m_sg_tk, self.p_dialog)]
            elif part == "animation":
                return [TargetSelector(),  ANINsLatestChekcer(), FrameRangeChecker(self.m_sg_tk), FPSChecker(self.m_sg_tk), ani_option_selector, AnimExporter(self.m_sg_tk, self.p_dialog)]
            elif part == "matchmove":
                import mmv_selector
                reload (mmv_selector)
                from mmv_selector import MMVSelector
                
                import mmv_exporter
                reload(mmv_exporter)
                from mmv_exporter import MMVExporter
                return [TargetSelector(),  FrameRangeChecker(self.m_sg_tk),ani_option_selector, FPSChecker(self.m_sg_tk), MMVSelector(), MMVExporter(self.m_sg_tk, self.p_dialog)]
            else:
                return [TargetSelector(),  FrameRangeChecker(self.m_sg_tk),ani_option_selector, FPSChecker(self.m_sg_tk), AnimExporter(self.m_sg_tk, self.p_dialog)]
                # return [TargetSelector(), GeoChecker(), FrameRangeChecker(self.m_sg_tk),ani_option_selector, AnimExporter(self.m_sg_tk, self.p_dialog)]

        elif part in ['lighting']:
            import target_selector
            reload(target_selector)
            from target_selector import TargetSelector

            import lgt_name_checker
            reload (lgt_name_checker)
            from lgt_name_checker import LGTNameChecker
            
            import lgt_exporter_02
            reload (lgt_exporter_02)
            from lgt_exporter_02 import LgtExporter
            
            return [TargetSelector(), LGTNameChecker(), LgtExporter(self.m_sg_tk, self.p_dialog)]

        elif part in ['characterfx', 'hair']:
            if search("set", LUCY.get_task()):
                import target_selector
                from target_selector import TargetSelector

                import hairSet_exporter
                reload(hairSet_exporter)
                from hairSet_exporter import HairSetExporter

                return [TargetSelector(), HairSetExporter(self.m_sg_tk, self.p_dialog)]
            else:
                import target_selector
                from target_selector import TargetSelector

                # geo checker(with mdl)(with rig, if there is...)
                import cfx_geo_checker
                # reload (cfx_geo_checker)
                from cfx_geo_checker import CFXGeoChecker

                import cfx_tex_checker
                reload(cfx_tex_checker)
                from cfx_tex_checker import CFXTexChekcer

                # name Checker
                import cfx_name_checker
                reload (cfx_name_checker)
                from cfx_name_checker import CFXNameChekcer

                import hair_selector
                reload(hair_selector)
                from hair_selector import HairSelector

                # exporter
                import cfx_exporter
                reload (cfx_exporter)
                from cfx_exporter import CFXExporter


                return [TargetSelector(), CFXNameChekcer(), CFXTexChekcer(), HairSelector(), CFXExporter(self.m_sg_tk, self.p_dialog)]

        elif part in ['simulation']:
            # import target_selector
            # # reload(target_selector)
            # from target_selector import TargetSelector

            # import frame_range_checker
            # # reload (frame_range_checker)
            # from frame_range_checker import FrameRangeChecker


            # import sim_selector
            # reload (sim_selector)
            # from sim_selector import SimSelector


            # import sim_exporter_v02
            # reload (sim_exporter_v02)
            # from sim_exporter_v02 import SimExporter


            # sim_option_selector = SimSelector()
            # sim_option_selector.refresh()

            
            import target_selector
            from target_selector import TargetSelector


            import frame_range_checker
            reload (frame_range_checker)
            from frame_range_checker import FrameRangeChecker


            # import anim_selector    # _v02
            # reload (anim_selector)  # _v02
            # from anim_selector import AnimSelector

            # import anim_exporter    # _v02
            # reload (anim_exporter)  # _v02
            # from anim_exporter import AnimExporter


            import anim_selector_v03    # _v02
            reload (anim_selector_v03)  # _v02
            from anim_selector_v03 import AnimSelector
            
            import anim_exporter_v03    # _v02
            reload (anim_exporter_v03)  # _v02
            from anim_exporter_v03 import AnimExporter


            
            ani_option_selector = AnimSelector()
            ani_option_selector.refresh()

            
            return [TargetSelector(), FrameRangeChecker(self.m_sg_tk), ani_option_selector, AnimExporter(self.m_sg_tk, self.p_dialog)]
        





        else:
            return []
