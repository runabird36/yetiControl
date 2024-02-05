
import maya.cmds as cmds
from traceback import print_exc

attr_list = [
                "yetiReferenceLength",
                "yetiReferencePositionX", "yetiReferencePositionY", "yetiReferencePositionZ",
                "yetiReferenceNormalX", "yetiReferenceNormalY", "yetiReferenceNormalZ"
            ]


def get_shapes_from_set(set_name :str) -> list:
    curve_list_of_set   = cmds.sets(set_name, q=True)
    cv_shapes_lis       = cmds.ls(curve_list_of_set, dag=True, ni=True, shapes=True)
    cv_shapes_lis.sort()
    return cv_shapes_lis


def do_attribute_copy(from_cv_shape :str, to_cv_shape :str) -> None:
    global attr_list
    for attr_name in attr_list:
        try:
            from_val = cmds.getAttr(f"{from_cv_shape}.{attr_name}")
            # print(from_val, type(from_val))
            # print(f"{to_cv_shape}.{attr_name}", type(f"{to_cv_shape}.{attr_name}"))
            cmds.setAttr(f"{to_cv_shape}.{attr_name}", from_val)
            
        except:
            print_exc()


def run() -> None:
    cv_set_grps = cmds.ls(os=True, ni=True, typ='objectSet', type="transform")
    # print(cv_set_grps)
    if len(cv_set_grps) != 2:
        cmds.confirmDialog(message="두개의 set을 선택해주십시오.")
        return
    
    from_cv_list = get_shapes_from_set(cv_set_grps[0])
    to_cv_list   = get_shapes_from_set(cv_set_grps[1])
    
    if len(from_cv_list) != len(to_cv_list):
        count_diff = abs(len(from_cv_list) - len(to_cv_list))
        cmds.confirmDialog(message=f"{count_diff} 의 갯수만큼 커브 갯수가 차이가 있습니다.\n갯수를 맞춰주십시오.")
        return


    for _f_long_name, _t_long_name in zip(from_cv_list, to_cv_list):
        _f_short_name = _f_long_name.split("|")[-1]
        _t_short_name = _t_long_name.split("|")[-1]
        print(f"{_f_short_name} -> {_t_short_name}")

        do_attribute_copy(_f_long_name, _t_long_name)
    
    # for x in range(len(from_cv_list)):
    #     _f_long_name    = from_cv_list[x]
    #     _t_long_name    = to_cv_list[x]

    #     _f_short_name   = _f_long_name.split("|")[-1]
    #     _t_short_name   = _t_long_name.split("|")[-1]
    #     print(f"{_f_short_name} -> {_t_short_name}")

    #     do_attribute_copy(_f_long_name, _t_long_name)


run()