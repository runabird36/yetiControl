
def create_yeti_group_cfx_ver(tar_assetname_GRP):
    re_ex_num = re.compile(r'[0-9]+$')
    asset_name = tar_assetname_GRP.split('_')[0]



    
    ns_num = neon.get_aniNS_from_geo(tar_assetname_GRP)
    if ns_num == '':
        # group_num = get_next_number(asset_name, group_num)
        group_num = "0"
        _res = re_ex_num.search(tar_assetname_GRP)
        if _res:
            group_num = str(int(_res.group()) + 1)
        else:
            group_num = "1"

        group_num = group_num.zfill(3)
    else:
        group_num = ns_num.split('_')[-1]

    grp_name = "{0}_{1}_yetiGRP".format(asset_name, group_num)
    if cmds.objExists(grp_name) == True:
        geo_exists_check = cmds.listRelatives(grp_name+'|geo', c=True)
        if geo_exists_check != []:
            cmds.parent(geo_exists_check, w=True)
        cmds.delete(grp_name)
    else:
        pass
    top_group = cmds.group(em=True, n=grp_name)

    geo_group = cmds.group(em=True, p=top_group ,n="geo")
    yeti_group = cmds.group(em=True, p=top_group ,n="yeti")
    grm_group = cmds.group(em=True, p=top_group ,n="grm")

    cmds.parent(tar_assetname_GRP, geo_group)



    return top_group, group_num