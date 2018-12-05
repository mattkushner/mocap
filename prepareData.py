import os
import maya.cmds as mc
import maya.mel as mel


def setup_mocap():
    fps = "120fps"
    src_path = "//gary/main/JOBS/1844N_Intel_CES/3D/ASSETS/Motion_Capture/20181126_DP/FBX/"
    dest_path = "//gary/main/JOBS/1844N_Intel_CES/3D/SOFTWARE/MAYA/STREETLIGHT_PREVIZ/scenes/mocap/"
    fbxs = os.listdir(src_path)
    for fbx in fbxs:
        # load fbx and save scene
        fbx_path = os.path.join(src_path, fbx)
        mb_path = os.path.join(dest_path, fbx.replace('.fbx', '.mb'))
        mc.file(force=True, new=True)
        mc.currentUnit(time=fps)
        mel.eval("SavePreferences;")
        mel.eval('file -import "'+file_path+'";')
        # remove namespaces in prep for label_joints()
        mc.namespace(moveNamespace=['eActor_v002:Solving', ':'])
        mc.namespace(removeNamespace='eActor_v002:Solving')
        mc.namespace(removeNamespace='eActor_v002')
        all_ws = mc.ls(assemblies=True)
        hips = mc.ls(assemblies=True, tail=len(all_ws)-4)
        if hips and len(hips)==1:
            label_joints(hips[0])
            mc.file(rename=mb_path)
            mc.file(save=True, force=True, options="v=0;", type="mayaBinary")

def label_joints(root_jnt):
    # enable HIK Controls
    mel.eval('HIKCharacterControlsTool;')
    # label joints, reset rotates
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
    # Create Character1 definition, connect to hips, load mocap_skeleton template
    mel.eval('hikCreateDefinition();')
    mel.eval('setCharacterObject("Hips","Character1",1,0);')

    
def load_mocap():
    mb_root = "//gary/main/JOBS/1844N_Intel_CES/3D/SOFTWARE/MAYA/STREETLIGHT_PREVIZ/scenes/mocap/"
    emma_file = "rp_emma_rigged_011_HIK_native.mb"
    dennis_file = "rp_dennis_rigged_004_HIK_native.mb"
    emma_path = os.path.join(mb_root, emma_file)
    dennis_path = os.path.join(mb_root, dennis_file)
    mbs = os.listdir(mb_root)
    for mb in mbs:
        if mb not in [emma_file, dennis_file]:
            suffix = 'emma'
            if mb.startswith('fem'):
                open_path = emma_path
                suffix = 'emma'
            elif mb.startswith('male'):
                open_path = dennis_path
                suffix = 'dennis'
            elif mb.startswith('cyclist'):
                open_path = dennis_path
                suffix = 'dennis'
            elif mb.startswith('pirouette'):
                open_path = emma_path
                suffix = 'emma'
            else:
                print(mb)
            import_path = os.path.join(mb_path, mb)
            mc.file(open_path, force=True, open=True)
            mel.eval('file -import "'+import_path+'";')
            mb_path = import_path.replace('.mb', '_'+suffix+'.mb')
            mc.file(rename=mb_path)
            mc.file(save=True, force=True, options="v=0;", type="mayaBinary")
            
