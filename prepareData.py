import maya.cmds as mc
import maya.mel as mel

jnts = mc.listRelatives('Hips', allDescendents=True) +['Hips']
for jnt in jnts:
    mc.select(jnt, replace=True)
    mc.setAttr(jnt+'.rotate',0,0,0)
    # single named joints
    if jnt in ['Head', 'Neck']:
        mel.eval('retargetingLimbLabel "'+jnt+'";')
    if jnt == 'Hips':
        mel.eval('retargetingLimbLabel "Root";')
    if 'Spine' in jnt:
        mel.eval('retargetingLimbLabel "Spine";')
    for side in ['Left', 'Right']:
        if side in jnt:
            mel.eval('retargetingSideLabel "'+side+'";')
            no_side_jnt = jnt.replace(side,'')
            if no_side_jnt == 'Arm':
                mel.eval('retargetingLimbLabel "Arm";')
            if no_side_jnt == 'Shoulder':
                mel.eval('retargetingLimbLabel "Collar";')     
            if no_side_jnt == 'UpLeg':
                mel.eval('retargetingLimbLabel "Leg";') 
