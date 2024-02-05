import maya.cmds as cmds

selected_grms = cmds.ls(sl=True, ni=True, typ='pgYetiGroom')
print(selected_grms)
