


import maya.cmds as cmds
from pprint import pprint

import YTX2New_toolkit
import importlib
importlib.reload(YTX2New_toolkit)

class YetiData():
    _yeti_node = ''
    _groom_list = []
    _shape_list = []
    _shape_pair_list = []
    _shape_texRef_list = []
    _shape_tarShape_list = []
    _shape_pair_list_temp = []
    _mat_info = ''
    _grm_path = ''

    _is_curve_type = False
    _set_and_curves_list = []
    _image_search_path = ''
    set_shape_texRef_list = []

    _return_str_template = '[Yeti name] : {YETI_NODE}\n\n'+\
                '[Groom nodes] : {GROOM_NODES}\n'+\
                '[Material name] : {MAT_NODES}\n\n'+\
                '[Shape texRef] : {SHAPE_TEXREF}\n'+\
                '[Shape tarShape] : {SHAPE_TARSHAPE}\n'+\
                '[.grm path] : {GRM_PATH}\n'

    def __init__(self, yeti_node='', groom_list=[], shape_list=[], mat_info='', grm_path='',
                is_curve_type=False, set_and_curves_list=[], image_search_path='', shape_and_grm_list=[], render_denstiy=1.0, float_var_list=[], vector_var_list=[]):
        self._yeti_node = yeti_node
        self._groom_list = groom_list
        self._shape_list = shape_list
        self._mat_info = mat_info
        self._grm_path = grm_path

        self._is_curve_type = is_curve_type
        self._set_and_curves_list = set_and_curves_list
        self._image_search_path = image_search_path
        self._render_density = render_denstiy
        self._shape_and_grm_list = shape_and_grm_list

        self._shape_pair_list_temp = []
        self.set_shape_pair_list(self._shape_list)
        self.set_shape_tarShape_list()
        self.set_shape_texRef_list()

        self._float_var_list = float_var_list
        self._vector_var_list = vector_var_list


    def __str__(self):
        _return_str = self._return_str_template.format(**{
                                    "YETI_NODE" : self._yeti_node,
                                    "GROOM_NODES": self.list_2_str(self._groom_list),
                                    "MAT_NODES": self._mat_info,
                                    "SHAPE_TEXREF": self.list_2_str(self._shape_texRef_list),
                                    "SHAPE_TARSHAPE": self.list_2_str(self._shape_tarShape_list),
                                    "GRM_PATH" : self._grm_path
                                    })
        return '+'*50 + '\n' + _return_str + '+'*50


    def list_2_str(self, _from_list):
        # print(_from_list)
        _to_str = '\n'
        for _element in _from_list:
            _to_str += (_element + '\n')
        return _to_str



    def get_yeti_node(self):
        return self._yeti_node

    def get_hair_mat(self):
        return self._mat_info


    def get_groom_list(self):
        return self._groom_list

    def get_grm_path(self):
        return self._grm_path

    def get_tex_ref_list(self):
        return self._shape_texRef_list

    def get_tar_shape_list(self):
        return self._shape_tarShape_list

    def get_shape_pair_list(self):
        return self._shape_pair_list


    def is_curve_sim(self):
        return self._is_curve_type

    def get_setCurves_list(self):
        return self._set_and_curves_list

    def get_image_search_path(self):
        return self._image_search_path

    def get_render_denstiy(self):
        return self._render_density

    def get_shape_and_grm_list(self):
        return self._shape_and_grm_list


    def get_float_var_list(self):
        return self._float_var_list

    def get_vector_var_list(self):
        return self._vector_var_list






    def set_shape_pair_list(self, whole_shape_list):
        for _shape_info in whole_shape_list:
            self._shape_pair_list_temp.append(_shape_info.get("EACH_shape"))
            self._shape_pair_list_temp.append(_shape_info.get("EACH_texRef"))

        # print(whole_shape_list)
        # print(self._shape_pair_list_temp)
        # print(self._shape_pair_list)

        self._shape_pair_list = list(zip(self._shape_pair_list_temp[0::2], self._shape_pair_list_temp[1::2]))


    def set_shape_tarShape_list(self):
        self._shape_tarShape_list = self._shape_pair_list_temp[0::2]


    def set_shape_texRef_list(self):
        self._shape_texRef_list = self._shape_pair_list_temp[1::2]



    def disconnect_and_delete_all(self):
        _del_tar = []
        _disconnect_tar = []

        _yeti_node = self.get_yeti_node()
        _yeti_node = _yeti_node.split('Shape')[0] + '*' + 'Shape'
        _disconnect_tar.extend(cmds.ls(_yeti_node,l=True))


        _groom_list = self.get_groom_list()
        for _groom in _groom_list:
            _groom = _groom.split('Shape')[0] + '*' + 'Shape'
            # _disconnect_tar.append(_groom)
            _disconnect_tar.extend(cmds.ls(_groom,l=True))

        _texRef_list = self.get_tex_ref_list()
        for _tex_ref in _texRef_list:
            _tex_ref = _tex_ref.split('Shape')[0] + '*_reference'
            _del_tar.append(_tex_ref)

        # _tar_shape_list = self.get_tar_shape_list()
        # for _tar_shape in _tar_shape_list:
        #     _tar_shape = _tar_shape.split('Shape')[0] + '*'
        #     _del_tar.append(_tar_shape)

        pprint(_disconnect_tar)
        _del_tar.append(self.get_hair_mat())

        for _tar in _del_tar:
            if cmds.objExists(_tar) == True:
                cmds.delete(_tar)

        if _disconnect_tar == []:
            return
        YTX2New_toolkit.disconnect_linked_attr(_disconnect_tar)
        if cmds.objExists('yeti_backup_nodes') == False:
            cmds.group(_disconnect_tar, n='yeti_backup_nodes')
        else:
            
            backuped_list = cmds.listRelatives('yeti_backup_nodes', c=True, f=True, ad=True, typ=['pgYetiMaya', 'pgYetiGroom'])
            
            not_backuped_list = list(set(_disconnect_tar)-set(backuped_list))
            # print 111111111111111
            # print _disconnect_tar
            # print backuped_list
            # print not_backuped_list
            if len(not_backuped_list) == 0:
                return
            cmds.parent(not_backuped_list, 'yeti_backup_nodes')

        cmds.setAttr('yeti_backup_nodes.visibility', 0)
