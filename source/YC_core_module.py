
from maya.cmds import ls





__PUB_PATH_TEMPLATE__ = "{input_dirpath}/{pub_ext}/{assetname}_cfx.{pub_ext}"






def get_assetname(input_name :str="") -> str:
    _assetname = ""
    if input_name == "":
        selected_tars = ls(sl=True)
        if not selected_tars:
            return ""
        _assetname = selected_tars[0].split("_")[0]
    else:
        _assetname = input_name.split("_")[0]
    return _assetname






def get_pub_paths(input_dir :str, assetname :str, pub_ext :str) -> str:
    global __PUB_PATH_TEMPLATE__
    if "." in pub_ext:
        pub_ext = pub_ext.replace(".", "")
    
    pub_fullpath = __PUB_PATH_TEMPLATE__.format(
                                                    input_dirpath   = input_dir,
                                                    pub_ext         = pub_ext,
                                                    assetname       = assetname
                                                )
    return pub_fullpath