import maya.mel as mel
import maya.cmds as cmds

def addSubdivision():
    '''
    Adds VRay subdivision to selected objets and sets the max subdiv level to 4 which is plenty for nearly every single case
    '''
    nodeList = cmds.ls(selection = True, dag=True, lf=True, type = 'mesh') # find shape nodes of current selection
    for node in nodeList:
        mel.eval('vray addAttributesFromGroup %s vray_subdivision 1' % node)
        mel.eval('vray addAttributesFromGroup %s vray_subquality 1' % node)
        cmds.evalDeferred("cmds.setAttr ('%s.vrayMaxSubdivs', 4)"% node)