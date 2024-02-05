
import __future__
from typing import List, Tuple
from general_md_3x import py_toolkit 
import maya.mel as mel
import maya.cmds as cmds
import os

_main_path = os.path.dirname(os.path.abspath(__file__))
_main_path = _main_path.replace("\\", "/")
_mel_path = _main_path + '/yt_mel.mel'

mel.eval('source "{0}"'.format(_mel_path))


class YetiCurveAttr():
    def __init__(self, _name :str="", _len :float=0.0, _pos :Tuple[float]=[], _nor :Tuple[float]=[]) -> None:
        self.node_name :str          = _name
        self.len       :float        = _len
        self.pos       :Tuple[float] = _pos
        self.nor       :Tuple[float] = _nor
        
    def empty(self) -> bool:
        if self.get_name() == "":
            return True
        else:
            return False
    
    def set_name(self, _name :str) -> None:
        self.node_name = _name
    def set_len(self, _len :float) -> None:
        self.len = _len
    def set_pos(self, _pos :Tuple[float]) -> None:
        self.pos = _pos
    def set_nor(self, _nor :Tuple[float]) -> None:
        self.nor = _nor
        
    def get_name(self) -> str:
        return self.node_name
    def get_len(self) -> float:
        return self.len
    def get_pos(self) -> Tuple[float]:
        return self.pos
    def get_nor(self) -> Tuple[float]:
        return self.nor
        
    def export_to_dict(self) -> dict:
        return {"curve":self.get_name(), "len":self.get_len(), "pos":self.get_pos(), "nor":self.get_nor()}
       
    def import_from_dict(self, imported_dict :dict) -> None:
        self.set_name(imported_dict["curve"])
        self.set_len(imported_dict["len"])
        self.set_pos(imported_dict["pos"])
        self.set_nor(imported_dict["nor"])
        
def does_save_guide_rest(node :str) -> bool:
    if cmds.nodeType(node) == "objectSet":
        check_tar =  cmds.ls(cmds.sets(node, q=True)[0], dag=True, ni=True,type="nurbsCurve")[0]
    elif cmds.nodeType(node) == "transform":
        check_tar = cmds.ls(node, dag=True, ni=True, type="nurbsCurve")[0]
    elif cmds.nodeType(node) == "nurbsCurve":
        check_tar = node
    
    if cmds.objExists(f"{check_tar}.yetiReferenceLength") == True:
        return True
    else:
        return False
        
def get_curve_info(tar :str) -> List[YetiCurveAttr]:
    '''
        tar : transform node which includes guide curves
    '''
    if does_save_guide_rest(tar) == False:
        return []
    
    if cmds.nodeType(tar) == "nurbsCurve":
        val_len = cmds.getAttr(f"{tar}.yetiReferenceLength")
        val_pos = cmds.getAttr(f"{tar}.yetiReferencePosition")
        val_nor = cmds.getAttr(f"{tar}.yetiReferenceNormal")
        return [YetiCurveAttr(tar, val_len, val_pos[0], val_nor[0])]
    else:
        targets  = []
        children = []
        if cmds.nodeType(tar) == "transform":
            children = cmds.listRelatives(tar, c=True)
        elif cmds.nodeType(tar) == "objectSet":
            children = cmds.sets(tar, q=True)
        for _node in children:
            targets.extend(get_curve_info(_node))
        return targets
        
        
def export_set_restpose(infos :List[YetiCurveAttr], to_path :str) -> str:
    to_json = []
    for _info in infos:
        to_json.append(_info.export_to_dict())
    py_toolkit.write_json(to_path, to_json)
    

def set_curve_restpose_attr(_info :YetiCurveAttr) -> None:
    tar_node = _info.get_name()
    real_names = cmds.ls(tar_node, l=True)
    if real_names == [] or real_names == None:
        return
    
    for _real_name in real_names:
        cmds.setAttr(f"{_real_name}.yetiReferenceLength", _info.get_len())
        cmds.setAttr(f"{_real_name}.yetiReferencePosition", _info.get_pos()[0], _info.get_pos()[1], _info.get_pos()[2], type="double3")
        cmds.setAttr(f"{_real_name}.yetiReferenceNormal",   _info.get_nor()[0], _info.get_nor()[1], _info.get_nor()[2], type="double3")  

def import_set_restpose(info_path :str) -> None:
    curve_infos = py_toolkit.read_json(info_path)
    
    for _info in curve_infos:
        yeti_attr = YetiCurveAttr()
        yeti_attr.import_from_dict(_info)
        
        set_curve_restpose_attr(yeti_attr)
        
        


def update_set_name(y_node, from_set, to_set):

    mel.eval('updateSetName(\"{0}\", \"{1}\", \"{2}\")'.format(
                                                            y_node,
                                                            from_set,
                                                            to_set))


def create_yeti_node(node_name):
    return mel.eval('create_yeti_without_addmesh_v02(\"{0}\")'.format(node_name))



def add_basemesh_to_yeti(tar_yeti_node, tar_basemesh):
    mel.eval('pgYetiAddGeometry( \"{0}\", \"{1}\" );'.format(tar_basemesh,
                                                            tar_yeti_node))



def add_set_to_yeti(tar_yeti_node, tar_setname):
    mel.eval("pgYetiAddGuideSet(\"{0}\", \"{1}\")".format(tar_setname, tar_yeti_node))




def import_groom_from_yeti(tar_grm, tar_basemesh, tar_yeti):
    return mel.eval("import_groomFile_from_yNode_v03(\"{0}\", \"{1}\", \"{2}\")".format(tar_grm,
                                                                                        tar_basemesh,
                                                                                        tar_yeti))
def get_info_from_yeti( yeti_node :str, info_type :str="all") -> list:
    '''
    - info_type : str
        mesh / pgYetiGroom / objectSet
    '''
    if info_type == "all":
        return cmds.listConnections(yeti_node, d=False, s=True, sh=True)
    else:
        return cmds.listConnections(yeti_node, d=False, s=True, sh=True, type=info_type)



def to_long_name(func):
    def is_longname(cur_name):
        if "|" in cur_name:
            return True
        else:
            return False
    def decorated(*args, **kwargs):
        y_node_name = kwargs["yeti_name"]
        if is_longname(y_node_name) == False:
            res = cmds.ls(y_node_name, l=True)
            y_node_name = res[0]
        kwargs["yeti_name"] = y_node_name
        print("Target Node : ", y_node_name)
        res = func(**kwargs)
        return res
    return decorated

@to_long_name
def get_yeti_imageSearchPath(yeti_name :str) -> str:
    attr_name = yeti_name + "." + "imageSearchPath"
    return cmds.getAttr(attr_name)
    

@to_long_name
def set_yeti_imageSearchPath(yeti_name :str, isp_path :str) -> str:
    if isp_path == None:
        return
    attr_name = yeti_name + "." + "imageSearchPath"
    cmds.setAttr(attr_name, isp_path, type="string")
    

@to_long_name
def get_yeti_cachepath(yeti_name :str) -> str:
    attr_name = yeti_name + "." + "cacheFileName"
    return cmds.getAttr(attr_name)
    

@to_long_name
def set_yeti_cachepath(yeti_name :str, cache_path :str) -> str:
    attr_name = yeti_name + "." + "cacheFileName"
    cmds.setAttr(attr_name, cache_path, type="string")
    
