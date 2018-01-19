#Author-
#Description-

import adsk.core, adsk.fusion, adsk.cam, traceback

def print_point(point: adsk.core.Point3D, message: str):
    
        app = adsk.core.Application.get()
        ui  = app.userInterface
        ui.messageBox(message + ': ' + str(point.x) + ', ' + str(point.y)  + 
            ', ' + str(point.z))
        
    
    
def run(context):
    ui = None
    try:
        
        app = adsk.core.Application.get()
        ui  = app.userInterface
        
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        if not design:
            ui.messageBox('It is not supported in current workspace, please change to MODEL workspace and try again.')
            return
        
        sel = ui.selectEntity('Select a path to create a hole', 'Edges,SketchCurves')
        selObj = sel.entity
        
        if selObj.objectType != adsk.fusion.BRepEdge.classType():
            return
        
        edge = adsk.fusion.BRepEdge.cast(selObj)
        
        this_occurrence = edge.assemblyContext
        
        holes = adsk.fusion.HoleFeatures.cast(this_occurrence.component.features.holeFeatures)
        
        start_vertex = edge.startVertex
        
#        print_point(start_vertex.geometry, 'Start Vertex')
        
#        asm_vertex = start_vertex.createForAssemblyContext(this_occurrence)
#        
#        print_point(asm_vertex.geometry, 'Asm Vertex')

        start_geom = start_vertex.geometry.copy()
        
        vector = adsk.core.Vector3D.create(.1, .1, 0)
        
        start_geom.translateBy(vector)
        
#        print_point(start_geom, 'Translated Point')
        
        offset = adsk.core.ValueInput.createByString('.25 in')
        
        sel = ui.selectEntity('Select Edge 1', 'Edges')
        edge1 = sel.entity
        
        sel = ui.selectEntity('Select Edge 2', 'Edges')
        edge2 = sel.entity
        
        sel = ui.selectEntity('Select Face (must be start)', 'Faces')
        face = sel.entity
        
        #create hole attributes
        holeInput = holes.createSimpleInput(adsk.core.ValueInput.createByString('1 in'))
        holeInput.tipAngle = adsk.core.ValueInput.createByString('180 deg')
        holeInput.isDefaultDirection = True
        holeInput.creationOccurrence = this_occurrence  #this parameter doesn't appear to work!!
        propertyValue = holeInput.creationOccurrence
        ui.messageBox(str(propertyValue.name))
        holeInput.participantBodies = [edge.body]
        holeInput.setPositionByPlaneAndOffsets(face, start_geom, edge1, offset, edge2, offset)
        holeInput.setDistanceExtent(adsk.core.ValueInput.createByReal(edge.length)) 
#        holeInput.setOneSideToExtent(extentToEntity,False) 
        hole = holes.add(holeInput)
        
        

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
