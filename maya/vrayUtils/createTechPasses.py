import maya.cmds as cmds
import maya.mel as mel

def createTechPasses():
    '''
    Creates tech passes for rendering
    zdepth, xyz, normals, gi, spec, reflection, lighting, uv, top/down
    TODO : topdown not working well due to strange creation methods
    '''

    # first we make the sampler node as we will use this twice
    samplerNodeName = 'util_sampler_node'
    if not cmds.objExists(samplerNodeName) :
        samplerNode = cmds.shadingNode('samplerInfo', asUtility=True)
        samplerNode = cmds.rename(samplerNode, samplerNodeName)
    layerToMake = 'P'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
        cmds.rename (renderElement,layerToMake)
        cmds.setAttr (layerToMake + '.vray_explicit_name_extratex', 'Pworld', type = 'string')
        cmds.setAttr (layerToMake + '.vray_considerforaa_extratex', 0)
        cmds.connectAttr (samplerNode + '.pointWorld', 'Pworld.vray_texture_extratex')
    layerToMake = 'Pcam'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
        cmds.rename (renderElement,layerToMake)
        cmds.setAttr (layerToMake + '.vray_explicit_name_extratex', 'Pcam', type = 'string')
        cmds.setAttr (layerToMake + '.vray_considerforaa_extratex', 0)
        cmds.connectAttr (samplerNode + '.pointCamera', 'Pcam.vray_texture_extratex')
        
    # layerToMake = 'Pobj'
    # if not cmds.objExists(layerToMake) :
    #     renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
    #     cmds.rename (renderElement,layerToMake)
    #     cmds.setAttr (layerToMake + '.vray_explicit_name_extratex', 'Pobj', type = 'string')
    #     cmds.setAttr (layerToMake + '.vray_considerforaa_extratex', 0)
    #     cmds.connectAttr (samplerNode + '.pointObject', 'Pobj.vray_texture_extratex')



    # now we make the normals render element
    layerToMake = 'N'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval ('vrayAddRenderElement normalsChannel;')
        cmds.rename (renderElement,layerToMake)
        cmds.setAttr(layerToMake + '.vray_filtering_normals', 0)
    # uv render element
    layerToMake = 'uv'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
        cmds.rename (renderElement,layerToMake)
        cmds.setAttr (layerToMake + '.vray_explicit_name_extratex', 'uv', type = 'string')
        cmds.connectAttr (samplerNode + '.uvCoord.uCoord', layerToMake + '.vray_texture_extratex.vray_texture_extratexR')    
        cmds.connectAttr (samplerNode + '.uvCoord.vCoord', layerToMake + '.vray_texture_extratex.vray_texture_extratexG')
        cmds.setAttr(layerToMake + '.vray_filtering_extratex', 0)
    # add zdepth unclamped and unfiltered
    layerToMake = 'zdepth'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval('vrayAddRenderElement zdepthChannel;')
        renderElement = cmds.rename (renderElement, layerToMake)
        cmds.setAttr(renderElement + '.vray_depthClamp', 0)
        cmds.setAttr(renderElement + '.vray_filtering_zdepth', 0)
    # add zdepth filtered
    layerToMake = 'zdepthAA'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval('vrayAddRenderElement zdepthChannel;')
        renderElement = cmds.rename (renderElement, layerToMake)
        cmds.setAttr(renderElement + '.vray_name_zdepth', layerToMake, type = 'string') 
        cmds.setAttr(renderElement + '.vray_depthClamp', 0)
        cmds.setAttr(renderElement + '.vray_filtering_zdepth', 1)    
    # add base render layers for recomp
    layerToMake = 'gi'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval('vrayAddRenderElement giChannel;')
        renderElement = cmds.rename (renderElement, layerToMake)
        cmds.setAttr (renderElement + '.vray_name_gi', layerToMake, type = 'string')
    layerToMake = 'lighting'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval('vrayAddRenderElement lightingChannel;')
        renderElement = cmds.rename (renderElement, layerToMake)
    layerToMake = 'reflection'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval('vrayAddRenderElement reflectChannel;')
        renderElement = cmds.rename (renderElement, layerToMake)
    layerToMake = 'specular'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval('vrayAddRenderElement specularChannel;')
        renderElement = cmds.rename (renderElement, layerToMake)
    # create top down
    layerToMake = 'topdown'
    if not cmds.objExists (layerToMake) :
        renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
        renderElement = cmds.rename (renderElement,layerToMake)
        cmds.setAttr(renderElement + '.vray_explicit_name_extratex', 'topdown', type = 'string') 
        newNode = mel.eval('$node = `shadingNode -asTexture -name "topdown_tex" VRayPluginNodeTex`;\
        vray addAttributesFromDll $node "texture" "TexFalloff";\
        int $placement = 2;\
        vrayCreateNodeFromDll_connectUVW $node $placement;\
        ')
        cmds.evalDeferred("cmds.setAttr (('{0}.direction_type'.format('topdown_tex')), 2)", lowestPriority=True)
        cmds.evalDeferred("cmds.setAttr (('{0}.color1'.format('topdown_tex')), 1, 0, 0,  type='double3')", lowestPriority=True)
        cmds.evalDeferred("cmds.setAttr (('{0}.color2'.format('topdown_tex')), 0, 1, 0,  type='double3')", lowestPriority=True)
        cmds.evalDeferred("cmds.connectAttr (('{0}.outColor'.format('topdown_tex')), '{0}.vray_texture_extratex'.format('topdown'))", lowestPriority=True)
        
    # create AO
    layerToMake = 'ao'
    if not cmds.objExists(layerToMake) :
        renderElement = mel.eval ('vrayAddRenderElement ExtraTexElement;')
        renderElement = cmds.rename (renderElement,layerToMake)
        cmds.setAttr (renderElement + '.vray_explicit_name_extratex', layerToMake, type = 'string')
        newNode = cmds.shadingNode('VRayDirt', name = 'ao_tex', asTexture=True)
        cmds.connectAttr (newNode + '.outColor', renderElement + '.vray_texture_extratex')
        cmds.setAttr (newNode + '.invertNormal', 1)
        cmds.setAttr (newNode + '.ignoreForGi', 0)
        cmds.setAttr (newNode + '.blackColor', -0.5 ,-0.5 ,-0.5, type='double3')
        cmds.setAttr (newNode + '.falloff', 5)
        
        
