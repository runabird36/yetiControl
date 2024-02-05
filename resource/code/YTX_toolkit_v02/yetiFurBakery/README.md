# YetiFurBakery
---

## 기능 명세
- fur bake
- sg 등록
- deadline submit
- control yeti
	- yeti 노드만 모아서 보기
	- fur cache 를 불러온 yeti 그룹을 따로 만들고 왔다갔다 전환


## 규약
```
- 경로 만들때, 고려되어야하는 요소 항목들
shotnum / namespace(kadan_002) / yetiname / taskname / vernum / ext(fur)

- dev 경로 규약
{@shot_root}/simulation/{taskname_code}/dev/cache/fur/{bakeversion_code}/{namespace}_{yetiname}.%04d.fur

- pub 경로 규약
{@shot_root}/simulation/{taskname_code}/pub/fur/{pubversion_code}/{namespace}_{yetiname}.%04d.fur
```

## Input 
- 현재 경로
- shotnum / taskname / version num / namespace / yeti name
- target list <- remove, add, clear all
- frame in / frame out / samples

## 핵심 코드
```
import maya.cmds as cmds
import maya.mel as mel
import os, re
import LUCY

def name_setting(func):
    def to_cachename(tar):
        cache_name = tar.split('_')[1]
        cmds.rename(tar, cache_name)
        return cache_name
        
    def get_namespace(tar):
        word_list = tar.split("_")
        assetname = word_list[0]
        ns_num = word_list[-1]
        ns_num = re.sub(r"[a-zA-Z]+", "", ns_num)
        print(ns_num)
        return assetname+"_"+ns_num
        
    def to_cachename_v02(tar, cur_ns):
        temp01 = tar.split("_YETI")[0]
        temp02_list = temp01.split("_")
        temp02_list.pop(0)
        cache_name = '_'.join(temp02_list)
        cache_name = cur_ns+"_"+cache_name

        cmds.rename(tar, cache_name)
        return cache_name
        
    def to_origin_name(tar, origin_name):
        cmds.rename(tar, origin_name)
        
        
    def decorated(*args, **kwargs):
        yeti_list = kwargs["tar_list"]
        changed_name_list = []
        for yeti_node in yeti_list:
            cur_ns = get_namespace(yeti_node)
            res = to_cachename_v02(yeti_node, cur_ns)
            changed_name_list.append(res)
        kwargs["cache_name_list"] = changed_name_list
        func(**kwargs)
        for origin, changed in zip(yeti_list, changed_name_list):
            to_origin_name(changed, origin)
        
    return decorated
    
    
def get_selected_yeti():
    return cmds.ls(sl=True, ni=True, dag=True, type="pgYetiMaya")
    

    
@name_setting
def bake_fur(**kwargs):
    
    print("Input parms : ", kwargs)
    tar_list     = kwargs["cache_name_list"]
    path_dir     = kwargs["path_dir"]
    frame_in     = kwargs["frame_in"]
    frame_out    = kwargs["frame_out"]
    samples      = kwargs["samples"]
    
    if os.path.exists(path_dir) == False:
        os.makedirs(path_dir)
    
    cmds.select(tar_list)
    print("Bake targets : ", tar_list)
    bake_cmd = "pgYetiCommand -writeCache \"{DIRNAME}/<NAME>.%04d.fur\" -range {FRAME_IN} {FRAME_OUT} -samples {SAMPLES}".format(DIRNAME  = path_dir,
                                                                                                                                   FRAME_IN = frame_in,
                                                                                                                                   FRAME_OUT= frame_out,
                                                                                                                                   SAMPLES  = samples)
    print("Bake Command : ", bake_cmd)
    mel.eval(bake_cmd)
    
vernum = "v001"
pub_dir = LUCY.get_pub_dir()
pub_ver_dir = pub_dir + "/fur/" + vernum
print(pub_ver_dir)

seleted_nodes = get_selected_yeti() 
bake_fur(tar_list=seleted_nodes, path_dir=pub_ver_dir, frame_in="990", frame_out="1020", samples="3")
```