# A generic function to create element component from any reference IDs
# refIds    --> a list of geometry reference IDs
# groupName --> the name of the element component
# mesh      --> the mesh object
# stream    --> the stream to write the APDL commands
def createElementComponent(refIds,groupName,mesh,stream):
    iElementNumer = 0;
    for refId in refIds:
        meshRegion = mesh.MeshRegionById(refId)
        for elementId in meshRegion.ElementIds: iElementNumer += 1
    stream.WriteLine('CMBLOCK,{0},ELEMENT,      {1}', groupName, iElementNumer)
    stream.WriteLine('(8i10)')
    iCounter =0;
    for refId in refIds:
        meshRegion = mesh.MeshRegionById(refId)
        for elementId in meshRegion.ElementIds:
            element = mesh.ElementById(elementId)
            val = 0.
            iCounter += 1
            if iCounter % 8 == 0:
                stream.Write('% 10d' % elementId + "\n")
            else:
                stream.Write('% 10d' % elementId)
    stream.WriteLine()
