import os
import maya.cmds as mc
import maya.mel as mel


def setup_mocap():
    src_path = "//gary/main/JOBS/1844N_Intel_CES/3D/ASSETS/Motion_Capture/20181126_DP/FBX/"
    dest_path = "//gary/main/JOBS/1844N_Intel_CES/3D/SOFTWARE/MAYA/STREETLIGHT_PREVIZ/scenes/mocap/"
    for fbx in fbxs:
        # load fbx and save scene
        fbx_path = os.path.join(src_path, fbx)
        mb_path = os.path.join(dest_path, fbx.replace('.fbx', '.mb'))
        mc.file(force=True, new=True)
        mc.file(fbx_path, import=True, type="FBX", ignoreVersion=True, mergeNamespacesOnClash=False, rpr="pirouette_001", options="fbx", pr=True, importFrameRate=True,  importTimeRange="override")
        # remove namespaces in prep for label_joints()
        mc.namespace(moveNamespace=['eActor_v002:Solving', ':'])
        mc.namespace(removeNamespace='eActor_v002:Solving')
        mc.namespace(removeNamespace='eActor_v002')
        all_ws = mc.ls(assemblies=True)
        hips = mc.ls(assemblies=True, tail=len(all_ws)-4)
        if hips and len(hips)==1:
            label_joints(hips[0])
            mc.file(mb_path,  save=True, options="v=0;")

def label_joints(root_jnt):
    jnts = mc.listRelatives(root_jnt, allDescendents=True) +[root_jnt]
    for jnt in jnts:
        mc.select(jnt, replace=True)
        x = 0
        if jnt == 'Hips':
            x = -90
        mc.setAttr(jnt+'.rotate',x,0,0)
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
