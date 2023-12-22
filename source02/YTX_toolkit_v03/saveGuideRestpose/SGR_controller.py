
import maya.cmds as cmds
import maya.mel as mel
def _run():
    cur_asset_set_list = cmds.ls(sl=True, ni=True, typ='objectSet')
    

    # Save guide rest pose
    try:
        cmds.select(deselect=True)

        cmds.select(cur_asset_set_list)

        mel.eval("pgYetiCommand -saveGuidesRestPosition;")
    except Exception as e:
        print(str(e))
    cmds.confirmDialog( title='Confirm', message=u'Save guide rest position 완료!')
