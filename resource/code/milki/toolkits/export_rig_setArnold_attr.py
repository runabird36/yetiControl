import re
from pprint import pprint
import maya.cmds as cmds
shape_arnold_attr_target_list = ['aiOpaque',
                                    'aiMatte',
                                    'aiSubdivType',
                                    'aiSubdivIterations',
                                    'aiSubdivAdaptiveMetric',
                                    'aiSubdivPixelError',
                                    'aiSubdivAdaptiveSpace',
                                    'aiSubdivUvSmoothing',
                                    'aiSubdivSmoothDerivs',
                                    'aiSubdivFrustumIgnore',
                                    'aiDispHeight',
                                    'aiDispPadding',
                                    'aiDispZeroValue',
                                    'aiDispAutobump',
                                    'aiStepSize',
                                    'aiVolumePadding']


def set_ai_attr(_asset_name):
    print('='*50)
    print('Set arnold attribute')
    print('Asset name : {0}'.format(_asset_name))
    _target = '{0}_rig|geo|{0}_GRP'.format(_asset_name)
    print('Target : {0}'.format(_target))
    print('='*50)
    except_list = ['instancer', 'nParticle', 'nucleus', 'pointEmitter', 'pointLight', 'nurbsCurve', 'gpuCache', 'lattice', 'baseLattice']



    re_shape = re.compile('Shape$')

    # =======================================================================
    # query all shape long name to list
    # =======================================================================
    all_shape = cmds.ls(_target, dag=True, l=True, shapes=True)

    # =======================================================================
    # get only '~Shape' among the all list ( which is end with 'Shape')
    # =======================================================================
    only_shape_list = []
    deformed_shape_list = []
    for _each_shape in all_shape:

        _node_type = cmds.nodeType(_each_shape)
        if _node_type in except_list:
            continue

        res = re_shape.search(_each_shape)
        if res:
            only_shape_list.append(_each_shape)
        else:
            deformed_shape_list.append(_each_shape)


    # =======================================================================
    # Check and Get '~Deformed or ~Orig' if exists
    # and
    # Set Attr to them
    # =======================================================================
    for _shape in only_shape_list:
        duplicated_shape_list = cmds.ls(_shape + '*', l=True)
        duplicated_shape_list.remove(_shape)
        if duplicated_shape_list == []:
            continue

        for _ai_attr in shape_arnold_attr_target_list:
            cur_ai_attr = '.'.join([_shape, _ai_attr])
            cur_attr = cmds.getAttr(cur_ai_attr)

            for _dupl_shape in duplicated_shape_list:
                dupl_attr = '.'.join([_dupl_shape, _ai_attr])

                try:
                    cmds.setAttr(dupl_attr, cur_attr)
                except Exception as e:
                    print('='*50)
                    print(str(e))
                    print('='*50)
