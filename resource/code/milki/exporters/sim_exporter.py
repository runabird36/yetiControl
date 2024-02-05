
import exporter
# reload (exporter)
from exporter import Exporter

import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGuiOrig
import PySide2.QtWidgets as QtGui


import maya.cmds as cmds
import maya.mel as mel
import time, os


from maya_md import neon
from maya_md import wm_stamp
from general_md_3x import LUCY




_write_cache_template = 'pgYetiCommand -writeCache \"{CACHE_FULLPATH}\" -range {START_FRAME} {END_FRAME} -samples {SAMPLES};'

class YetiItem():
    def __init__(self):
        self.fur_export_target_path_dict ={}




    def get_top_level_from_yetishape(self, _tar_yeti_longname):
        for _address_component in _tar_yeti_longname.split('|'):
            if _address_component.endswith('_yetiGRP'):
                return _address_component

        return None





    def pre_do_item(self, m_sg_tk, targets, path_list):
        # ['X:/projects/2020_02_pipelineFX/sequence/CFX/CFX_0040/sim/pub/fur/pub_CFX_0040_sim.fur',
        # 'X:/projects/2020_02_pipelineFX/sequence/CFX/CFX_0040/sim/pub/fur/versions/pub_CFX_0040_sim_v10.fur']


        # shotName/sim/pub/cache/ycache/assetname_001/pub_shotName_sim_assetName_001.%04d.fur
        # shotName/ani/dev/cache/ycache/assetname_001/versions(scene)/pub_shotName_sim_v01_assetName_001.%04d.fur

        pub_fur_path = path_list[0]
        pub_fur_dirpath = pub_fur_path.split('/pub/')[0]
        pub_fur_basename = os.path.basename(pub_fur_path)


        for _tar in targets:

            tar_yeti_shortname = _tar.split('|')[-1]
            asset_name = tar_yeti_shortname.split('_')[0]
            component_info_temp = tar_yeti_shortname.replace(asset_name+'_', '')
            component_info = tar_yeti_shortname.replace('_YETIShape', '')
            component_info_for_basename = component_info_temp.replace('_YETIShape', '')

            yeti_top_level_group = self.get_top_level_from_yetishape(_tar)
            tar_ns = yeti_top_level_group.replace('_yetiGRP', '')
            cur_fur_basename = pub_fur_basename.replace('.fur', '_{1}_{3}.%04d.fur')
            cur_fur_path_template = '{0}/pub/cache/ycache/{1}/{2}/' + cur_fur_basename
            cur_fur_path = cur_fur_path_template.format(pub_fur_dirpath, tar_ns, component_info, component_info_for_basename)

            if not os.path.exists(os.path.dirname(cur_fur_path)):
                os.makedirs(os.path.dirname(cur_fur_path))

            self.fur_export_target_path_dict[_tar] = [cur_fur_path]



        return self.fur_export_target_path_dict




    def do_item(self, targets, options, task, user, path_list=None, additional_info=None):
        exportType = 'YETI_FUR'
        path_to_sg = []

        try:
            cmds.select(cl=True)
        except Exception as e:
            print(str(e))


        s_frame = options.get('Start Frame')[0]
        e_frame = options.get('End Frame')[0]
        samples = options.get('Samples')[0]



        for _yeti_tar, _bake_path in self.fur_export_target_path_dict.items():

            try:
                cmds.select(_yeti_tar)
            except Exception as e:
                print(str(e))
                return

            self.bake_fur_cache(_bake_path[0], s_frame, e_frame, samples)
            path_to_sg.append(_bake_path[0])

            _to_path_list = os.path.dirname(_bake_path[0])
            _to_path_list = os.path.dirname(_to_path_list)
            path_list.append(_to_path_list)


        export_info = [path_to_sg , exportType]
        return export_info







    def bake_fur_cache(self, fullpath, sframe, eframe, samples):
        make_cmd_dict = {}

        make_cmd_dict['CACHE_FULLPATH'] = fullpath
        make_cmd_dict['START_FRAME'] = sframe
        make_cmd_dict['END_FRAME'] = eframe
        make_cmd_dict['SAMPLES'] = str(int(float(samples)))

        write_dev_cache_cmd = _write_cache_template.format(**make_cmd_dict)

        print(write_dev_cache_cmd)

        mel.eval(write_dev_cache_cmd)






class SimExporter(Exporter):
    def __init__(self, m_sg_tk, p_dialog):
        Exporter.__init__(self)
        self.set_title("Exporter")
        self.m_sg_tk = m_sg_tk
        self.progress_dialog = p_dialog
        self.options = None
        self.targets = None
        # self.export_order_dict = {'playblast' : PlayblastItem(), 'alembic cache': AbcItem(), 'maya':MayaItem()}
        self.export_engine_dict = {'YETI':YetiItem()}
        self.export_targets_dict = {'YETI':[]}
        print('Exporter created')



    def pre_execute(self, targets, options):
        # get targets and options from milki_controller
        # if want to change or check target

        # print 333
        # print targets
        # print options
        self.targets = targets

        self.options = options
        self._set_basic_info()


        print(self.targets)

        self.make_long_name()
        self.select_engine()

        print(self.export_targets_dict)


        for _sim_type, _engine in self.export_engine_dict.items():
            if _sim_type == 'YETI':
                path_list = self.get_pub_paths('fur')
                _pub_targets = self.export_targets_dict.get('YETI')


            all_path=_engine.pre_do_item(self.m_sg_tk, _pub_targets, path_list)

            for path in all_path:
                self.add_pub_files(all_path[path])





    def execute(self):
        thumb = self.panel.get_thumb()
        desc = self.panel.get_desc()
        additional_info = [thumb, desc]
        self.check_pub_condition()

        # try:
        #     cmds.select(self.targets)
        # except Exception as e:
        #     print str(e)

        path_list = []
        for _sim_type, _engine in self.export_engine_dict.items():
            user = self.m_sg_tk.get_user()
            if _sim_type == 'YETI':
                _pub_targets = self.export_targets_dict.get('YETI')


            export_info = _engine.do_item(_pub_targets, self.options, self.tar_task, user, path_list, additional_info)
            path_to_sg = export_info[0]

            cur_scene_ver = LUCY.get_dev_vernum()
            self.pub_to_sg(path_to_sg, cur_dev_ver=cur_scene_ver)




        self.finish(path_list[0])











    def make_long_name(self):
        for _idx, _tar in enumerate(self.targets):
            if '|' in _tar:
                continue

            check_list = cmds.ls(_tar, l=True)
            if len(check_list)<2:
                self.targets[_idx] = cmds.ls(_tar, l=True)[0]
                continue

            if cmds.nodeType(check_list[0]) == 'pgYetiMaya':
                for _check in check_list:
                    if '|yeti|' in _check:
                        self.targets[_idx] = _check






    def select_engine(self):

        for _tar in self.targets:
            _node_typ = cmds.nodeType(_tar)
            if _node_typ == 'pgYetiMaya':
                self.export_targets_dict['YETI'].append(_tar)
