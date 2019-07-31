#
#	DODAC SPRAWDZENIE JEDNOSTEK

#
# mesh.ElementById(121).Dimension ????????? jak dla faces ulement i shela ??

#   SPRAWDZIC dlaczego jak element 2-order to blad wyskauje zamiast konczyc
#   moze dodac zeby wylaczal calkowice jak jest 2-order

#  dodac sprawdzenie danych importowanych
# jak blad to pokazuje error i koniec programu - np przez "exeption"
# - jak import np 2d jak jest 3d ustawione
# - jak 2 te same pliki

   	  
###########  KOMENDA DO USTAWIANIA ze HTC jest brane dla temp BULK !!!!!!!
  
##     if geoType == 'Named Selection': !!
  
########################################################################################################
########################################################################################################
########################################################################################################

from POINT__Lib import *
from READ_WRITE__Lib import *
from INTERPOLATION__Lib import *
from HTC_CALCULATION__Lib import *

import myUtils

import os
clr.AddReference("Ans.UI.Toolkit")
clr.AddReference("Ans.UI.Toolkit.Base")
from Ansys.UI.Toolkit import *

def EntryHTCClicked(currentAnalysis):
   load = currentAnalysis.CreateLoadObject("HTCLoad")

def writeLoadCommands(load,stream):


   ####################################
   #################################### KEYOPT 
   ####################################

   if load.Properties["SelectGeo"].Properties["SelectDimension"].ValueString=="3d":
   	Dimenions = 3
   	propGeo = load.Properties["SelectGeo"].Properties["SelectDimension"].Properties["GeoHTC_Face"]
   elif load.Properties["SelectGeo"].Properties["SelectDimension"].ValueString=="2d":
   	Dimenions = 2
    	propGeo = load.Properties["SelectGeo"].Properties["SelectDimension"].Properties["GeoHTC_Edge"]

   if propGeo.Value:
      geoType = propGeo.Properties['DefineBy'].Value
      if geoType == 'Named Selection':
   	   GeoRefNames = propGeo.Value.Name
      else:
   	   GeoRefIds = propGeo.Value.Ids

   stream.Write("\n/prep7\n\n")

   mesh = load.Analysis.MeshData
   geo = load.Analysis.GeoData

   ###################################
   ###################################
   
   #if geoType != 'Named Selection':
   #     myUtils.createElementComponent(GeoRefIds, "MyGrupe" + load.Id.ToString(), mesh, stream)
   #     stream.Write("CMSEL, S, MyGrupe" + load.Id.ToString() + "\n")
   #else:
   #     stream.Write("CMSEL,S,"+GeoRefNames+"\n")
   
   #stream.Write("*GET,n_el,ELEM,0,num,max\n")                 # take the highest element in selected set
   #stream.Write("*GET, Elem_Type, ELEM, n_el, ATTR, TYPE\n")  # take internal element type of the highest element "n_el"  
   #stream.Write("keyopt,Elem_Type,1,1\n")                     # designate keyopt(1) = 1 to selected element type

   #stream.Write("allsel, all\n")
   #stream.Write("/solu\n")
   
   ####################################
   ####################################
   
   
   for i,GeoRefId in enumerate(GeoRefIds):
      TempGeoRefId = []
      TempGeoRefId.append(GeoRefId)
      
      if geoType != 'Named Selection':
           myUtils.createElementComponent(TempGeoRefId, "MyGrupe" + str(i), mesh, stream)
           stream.Write("\nCMSEL, S, MyGrupe"  + str(i) + "\n")
      else:
           stream.Write("\nCMSEL,S,"+GeoRefNames+"\n")
      
      Elem_Type = "Elem_Type_" + str(i)
      n_el = "n_el_" + str(i)
      
      stream.Write("*GET,n_el_"+str(i)+",ELEM,0,num,max\n")                 # take the highest element in selected set
      stream.Write("*GET,Elem_Type_" + str(i)+", ELEM, n_el_"+str(i)+", ATTR, TYPE\n")  # take internal element type of the highest element "n_el"  
      stream.Write("keyopt,Elem_Type_" + str(i)+",1,1\n\n\n")                     # designate keyopt(1) = 1 to selected element type
   
   stream.Write("allsel, all\n")
   stream.Write("/solu\n")
   
   ####################################
   #################################### KEYOPT 
   ####################################
 

   MethodProp = load.Properties["SelectData"].Properties["MethodSelect"]
   if MethodProp.ValueString=="3 points":
   
      #    SFE, Elem, LKEY, Lab, KVAL, VAL1, VAL2, VAL3, VAL4
      ####  The simplest:
      #	   SFE, Elm_id, FACE_lkey, CONV, 0, 555  <- last HTC value
      #    SFE, Elm_id, FACE_lkey, CONV, 2, 120  <- last Bulk Temp in Celcjusz   
      ### Temp. dipendent HTC:
      #	   *DIM,TAB_ElmID,TABLE,2,1,1,TEMP
      #	   TAB_ElmID(1,0)=T1_celcjusz,T2_celcjusz
      #	   TAB_ElmID(1,1)=HTC_01,HTC_02
      #
      #	   SFE, Elm_id, FACE_lkey, CONV, 0, %TAB_ElmID%
      #    SFE, Elm_id, FACE_lkey, CONV, 2, Taw_celcjusz
    
      ElementsFinalList, H0,H1,TAW = GetData(load,False)
      ### ElementsFinalList = ElementWithEdge2d --> ElmId,FaceIdex,Node1Id,Node2Id,CenterPoint (Elm Id, X coord, Y coord)        
      
      ### if no 2-order elements
      if ElementsFinalList:
         ExtAPI.Log.WriteMessage("Writing Commands")
                  
         for i,Element in enumerate(ElementsFinalList):
            # stream.Write("SFE, " + str(Element.ElmId) + ", " + str(Element.FaceIdex) + ", CONV, 0, " + str(555) + "\n")
            # stream.Write("SFE, " + str(Element.ElmId) + ", " + str(Element.FaceIdex) + ", CONV, 2, " + str(120) + "\n\n")
       
            # wylicza HTC = h0 + h1*T !!! T w KELWINACH 
      
            T1_celcjusz = 20
            T2_celcjusz = 1000
            T1 = T1_celcjusz + 273.15
            T2 = T2_celcjusz + 273.15
      
            HTC_01 = H0[i] + H1[i]*T1; 
            HTC_02 = H0[i] + H1[i]*T2; 
      
            TAW_celcjusz = TAW[i] - 273.15;
      
            stream.Write("*DIM, TAB_" + str(Element.ElmId) + ", TABLE,2,1,1,TEMP\n")
            stream.Write("TAB_" + str(Element.ElmId) + "(1,0) = " + str(T1_celcjusz) + ", " + str(T2_celcjusz) + "\n")
            stream.Write("TAB_" + str(Element.ElmId) + "(1,1) = " + str(HTC_01) + ", " + str(HTC_02) + "\n\n")
      
            stream.Write("SFE, " + str(Element.ElmId) + ", " + str(Element.FaceIdex) + ", CONV, 0, %TAB_" + str(Element.ElmId) + "%\n")
            stream.Write("SFE, " + str(Element.ElmId) + ", " + str(Element.FaceIdex) + ", CONV, 2, " + str(TAW_celcjusz) + "\n\n")   
      else:
         MessageBox.Show("ERROR - 2 order elements")
         
   elif MethodProp.ValueString=="2 points":
  
      ElementsFinalList,HTC,TAW = GetData(load,False)
      
      ### if no 2-order elements
      if ElementsFinalList:
         ExtAPI.Log.WriteMessage("Writing Commands")       
         for i,Element in enumerate(ElementsFinalList):
      
            htc = HTC[i]
            TAW_celcjusz = TAW[i] - 273.15;
         
            stream.Write("SFE, " + str(Element.ElmId) + ", " + str(Element.FaceIdex) + ", CONV, 0, " + str(htc) + "\n")
            stream.Write("SFE, " + str(Element.ElmId) + ", " + str(Element.FaceIdex) + ", CONV, 2, " + str(TAW_celcjusz) + "\n\n")
      else:
         MessageBox.Show("ERROR - 2 order elements")
         
########################################################################################################
########################################################################################################
########################################################################################################

def ActionCheckData(load):
   GetData(load,True)

########################################################################################################
########################################################################################################
########################################################################################################

def GetData(load,WriteDataIndicator):

   PointsWhereToInterpolate = []
   H0 = []
   H1 = []
   TAW = []
   
   HTC2Points = []
   
   
   if load.Properties["SelectGeo"].Properties["SelectDimension"].ValueString=="3d":
   	Dimenions = 3
   	propGeo = load.Properties["SelectGeo"].Properties["SelectDimension"].Properties["GeoHTC_Face"]

   elif load.Properties["SelectGeo"].Properties["SelectDimension"].ValueString=="2d":
   	Dimenions = 2
    	propGeo = load.Properties["SelectGeo"].Properties["SelectDimension"].Properties["GeoHTC_Edge"]
   	
   PathFile01 = None
   PathFile02 = None
   PathFile03 = None

   MethodProp = load.Properties["SelectData"].Properties["MethodSelect"]
	
   PathFile01 = MethodProp.Properties["filename01"].ValueString
   PathFile02 = MethodProp.Properties["filename02"].ValueString
   PathFile03 = MethodProp.Properties["filename03"].ValueString

   if propGeo.Value:
        
      ElementsFinalList = GetElements(propGeo,Dimenions)
      ### 2d  # ElementsFinalList --> ElmId,FaceIdex,Node1Id,Node2Id,CenterPoint (Elm Id, X coord, Y coord)     
      ### 3d  # ElementsFinalList --> ElmId,FaceIdex,Node1Id,Node2Id,Node3Id,Node4Id,CenterPoint (Elm Id, X coord, Y coord)        	    
      
      ### if 2-order elements
      if ElementsFinalList == None:
         return
      
      if WriteDataIndicator:
         if Dimenions == 2:
            WriteDataToFile("C:\Users\Kamil\Desktop\Extenion_01\Interpolatetion_Points_Data.txt",["ElmId","FaceIdex","Node1Id","Node2Id","CenterX","CenterY"],[Elm.ElmId for Elm in ElementsFinalList],[Elm.FaceIdex for Elm in ElementsFinalList],[Elm.Node1Id for Elm in ElementsFinalList],[Elm.Node2Id for Elm in ElementsFinalList],[Elm.CenterPoint.x for Elm in ElementsFinalList],[Elm.CenterPoint.y for Elm in ElementsFinalList])
         elif Dimenions == 3:
            WriteDataToFile("C:\Users\Kamil\Desktop\Extenion_01\Interpolatetion_Points_Data.txt",["ElmId","FaceIdex","Node1Id","Node3Id","Node4Id","Node2Id","CenterX","CenterY"],[Elm.ElmId for Elm in ElementsFinalList],[Elm.FaceIdex for Elm in ElementsFinalList],[Elm.Node1Id for Elm in ElementsFinalList],[Elm.Node2Id for Elm in ElementsFinalList],[Elm.Node3Id for Elm in ElementsFinalList],[Elm.Node4Id for Elm in ElementsFinalList],[Elm.CenterPoint.x for Elm in ElementsFinalList],[Elm.CenterPoint.y for Elm in ElementsFinalList])

         ExtAPI.Log.WriteMessage("Points Data  Written - nodes where to interpolate")	
	
      for Elm in ElementsFinalList:
      	PointsWhereToInterpolate.append(Elm.CenterPoint)
     	
      	
      if MethodProp.ValueString=="3 points":
   	if PathFile01 and PathFile02 and PathFile03:
   	
     	   HeatFlux1,HeatFlux2,HeatFlux3,Temp1,Temp2,Temp3 = Interpolate(PointsWhereToInterpolate,
     	   			PathFile01,PathFile02,PathFile03,Dimenions,"3 points")	
    
           if WriteDataIndicator:
              AppendDataToFile("C:\Users\Kamil\Desktop\Extenion_01\Interpolatetion_Points_Data.txt",["HeatFlux1","HeatFlux2","HeatFlux3","Temp1","Temp2","Temp3"],HeatFlux1,HeatFlux2,HeatFlux3,Temp1,Temp2,Temp3)    	   
	      ExtAPI.Log.WriteMessage("Heat Flux Data Written")
	   
	   H0,H1,TAW,deltaM,MinusDeltaError = PrepareHTC_3Points(PointsWhereToInterpolate,HeatFlux1,HeatFlux2,HeatFlux3,Temp1,Temp2,Temp3)  
	      
	   if MinusDeltaError > 0:
   		MessageBox.Show("Error - Negative Discriminant")
   		
           if WriteDataIndicator:
	      AppendDataToFile("C:\Users\Kamil\Desktop\Extenion_01\Interpolatetion_Points_Data.txt",["H0","H1","TAW","Delta"],H0,H1,TAW,deltaM)
	      ExtAPI.Log.WriteMessage("HTC Preparation Data Written")
	 
	   return ElementsFinalList,H0,H1,TAW
	   
   	else:
   	   MessageBox.Show("No Input Data Files")

      elif MethodProp.ValueString=="2 points":
   	if PathFile01 and PathFile02:  
     	   HeatFlux1,HeatFlux2,Temp1,Temp2 = Interpolate(PointsWhereToInterpolate,
     	   			PathFile01,PathFile02,PathFile03,Dimenions,"2 points")
     	   			
           if WriteDataIndicator:
              AppendDataToFile("C:\Users\Kamil\Desktop\Extenion_01\Interpolatetion_Points_Data.txt",["HeatFlux1","HeatFlux2","Temp1","Temp2"],HeatFlux1,HeatFlux2,Temp1,Temp2)    	   
	      ExtAPI.Log.WriteMessage("Heat Flux Data Written")
	   
	   HTC2Points,TAW = PrepareHTC_2Points(PointsWhereToInterpolate,HeatFlux1,HeatFlux2,Temp1,Temp2)      	   			
           if WriteDataIndicator:
	      AppendDataToFile("C:\Users\Kamil\Desktop\Extenion_01\Interpolatetion_Points_Data.txt",["HTC","TAW"],HTC2Points,TAW)
	      ExtAPI.Log.WriteMessage("HTC Preparation Data Written")
	      
	   return ElementsFinalList,HTC2Points,TAW

   	else:
   	   MessageBox.Show("No input file")
   else:
      MessageBox.Show("No geometry selected")
   	
########################################################################################################
########################################################################################################
########################################################################################################

def GetElements(propGeo,Dimenions):
   
   ElementsFinalList = []
     
   if propGeo.Value:
      geoType = propGeo.Properties['DefineBy'].Value
      if geoType == 'Named Selection':
   	   GeoRefIds = propGeo.Value.Name
      else:
   	   GeoRefIds = propGeo.Value.Ids
           
      # Get the mesh of the model
      mesh = ExtAPI.DataModel.AnalysisList[0].MeshData
      # Loop on the list of the selected face id
      for GeoRefId in GeoRefIds:
  	   # Get mesh information for each face
   	   meshRegion = mesh.MeshRegionById(GeoRefId)
   	   IdOfElements = meshRegion.ElementIds
   	   
   	   #### CHECK ELEMENT ORDER
	   for IdOfElement in IdOfElements: 	   
       	      if mesh.ElementById(IdOfElement).CornerNodeCount != len(mesh.ElementById(IdOfElement).NodeIds):
    	         MessageBox.Show("ERROR - 2 order elements")
      	         return
      	            
   	   if Dimenions == 2:
   	   
    	      IdOfNodesOnCurve    = meshRegion.NodeIds   
  	   
	      for IdOfElement in IdOfElements:     
	      
	         IndexOfEdges, IdOfNodesOfEdges = CheckIsElementEdgeOnCurve(IdOfElement,IdOfNodesOnCurve)
	         if len(IndexOfEdges) > 0:
	            for i,IndexOfEdge in enumerate(IndexOfEdges):
	               # it is possible more than one the same element !
	            
	               Node1 = mesh.NodeById(IdOfNodesOfEdges[2*i-1])
	               Node2 = mesh.NodeById(IdOfNodesOfEdges[2*i])		
	  	       CenterPoint = Point2d(IdOfElement , (Node1.X + Node2.X)/2 , (Node1.Y + Node2.Y)/2 )

	               ElementsFinalList.append( ElementWithEdge2d(IdOfElement,IndexOfEdge,IdOfNodesOfEdges[2*i-1],IdOfNodesOfEdges[2*i],CenterPoint) )
	           
   	   elif Dimenions == 3:  	
   	   
	      Tri6Faces, Quad8Faces, Tri3Faces, Quad4Faces = meshRegion.GetFaces() ### lists of nodes of FACES which lie on surface
   	      
   	      if Tri3Faces:
   	         NumberOfElmsWithTriFaces = len(Tri3Faces)/3
   	      else:
   	         NumberOfElmsWithTriFaces = 0
   	       	      
   	      for z,IdOfElement in enumerate(IdOfElements):
   	         
   	         I=J=K=L=M=N=O=P= -1
   	         Faces = [[J,I,L,K],
   	         	  [I,J,N,M],
   	         	  [J,K,O,N],
   	         	  [K,L,P,O],
   	         	  [L,I,M,P],
   	         	  [M,N,O,P]]    	          	         
   	         
   	         CornerNodesOfElm = mesh.ElementById(IdOfElement).CornerNodeIds
   	         NumberOfCornerNodes = len(CornerNodesOfElm)
   	         
   	         if NumberOfCornerNodes == 6:     ### PRISM
   	         
   	            [I,J,K,M,N,O] = CornerNodesOfElm   	            
   	      	    Faces[0] = [J,I,K]   ### Face 1
   	            Faces[1] = [I,J,N,M] ### Face 2
   	            Faces[2] = [J,K,O,N] ### Face 3
   	            Faces[4] = [K,I,M,O] ### Face 5 	            	            
   	            Faces[5] = [M,N,O]   ### Face 6
   	            
   	         elif NumberOfCornerNodes == 4:   ### TET
   	         
   	            [I,J,K,M] = CornerNodesOfElm   	         
   	      	    Faces[0] = [J,I,K] ### Face 1
   	            Faces[1] = [I,J,M] ### Face 2
   	            Faces[2] = [J,K,M] ### Face 3   	            
   	            Faces[4] = [K,I,M] ### Face 5 	            	            
   	            
   	         elif NumberOfCornerNodes == 5:   ### PYRAMID
   	         
   	            [I,J,K,L,M] = CornerNodesOfElm
   	      	    Faces[0] = [J,I,L,K] ### Face 1
   	            Faces[1] = [I,J,M]   ### Face 2
   	            Faces[2] = [J,K,M]   ### Face 3
   	            Faces[3] = [K,L,M]   ### Face 4
   	            Faces[4] = [L,I,M]   ### Face 5
   	            
   	         elif NumberOfCornerNodes == 8:   ### HEX
   	         
   	            [I,J,K,L,M,N,O,P] = CornerNodesOfElm
   	      	    Faces[0] = [J,I,L,K]  ### Face 1
   	            Faces[1] = [I,J,N,M]  ### Face 2
   	            Faces[2] = [J,K,O,N]  ### Face 3
   	            Faces[3] = [K,L,P,O]  ### Face 4
   	            Faces[4] = [L,I,M,P]  ### Face 5    	            
   	            Faces[5] = [M,N,O,P]  ### Face 6   
   	            
   	         if (z+1) <=  NumberOfElmsWithTriFaces: ### <- if face is tri    	            
   	            Node1Id = Tri3Faces[z*3]
   	            Node2Id = Tri3Faces[z*3 + 1]
   	            Node3Id = Tri3Faces[z*3 + 2]
   	            Node4Id = 0 	            
   	            NodesId = [Node1Id,Node2Id,Node3Id,Node4Id]   	            
   	         elif (z+1) >  NumberOfElmsWithTriFaces: ### <- if face is quad
   	            Node1Id = Quad4Faces[(z - NumberOfElmsWithTriFaces)*4]
   	            Node2Id = Quad4Faces[(z - NumberOfElmsWithTriFaces)*4 + 1]
   	            Node3Id = Quad4Faces[(z - NumberOfElmsWithTriFaces)*4 + 2]
   	            Node4Id = Quad4Faces[(z - NumberOfElmsWithTriFaces)*4 + 3]
   	            NodesId = [Node1Id,Node2Id,Node3Id,Node4Id]
   	            
   	         for w,Face in enumerate(Faces):
   	            licznik = 0
   	            for NodeIdOfFace in Face:
   	            	for NodeId in NodesId:
   	            	   if NodeIdOfFace == NodeId:
   	            	      licznik += 1
   	            	      break
   	            if licznik >= 3:
   	               IndexOfFace = w+1
   	               break
   	         
	         Node1 = mesh.NodeById(Node1Id)
	         Node2 = mesh.NodeById(Node2Id)
	         Node3 = mesh.NodeById(Node3Id)
	         if Node4Id == 0:
	  	    CenterPoint = Point3d(IdOfElement,(Node1.X + Node2.X + Node3.X)/3 ,(Node1.Y + Node2.Y + Node3.Y)/3 ,(Node1.Z + Node2.Z + Node3.Z)/3)	         
	         elif Node4Id != 0:
	            Node4 = mesh.NodeById(Node4Id)	
	  	    CenterPoint = Point3d(IdOfElement,(Node1.X + Node2.X + Node3.X + Node4.X)/4 ,(Node1.Y + Node2.Y + Node3.Y + Node4.Y)/4 ,(Node1.Z + Node2.Z + Node3.Z + Node4.Z)/4)	         
   	              	                 	          
                 ElementsFinalList.append( ElementWithFace3d(IdOfElement,IndexOfFace,Node1Id,Node2Id,Node3Id,Node4Id,CenterPoint) )
	           

   return ElementsFinalList
	      	          	    	
########################################################################################################
########################################################################################################
########################################################################################################

def CheckIsElementEdgeOnCurve(IdOfElement,NodesOnCurve):

   # Check whether edge of element lies on curve
   # -> return idex of edges
   
   IndexOfEdges = []
   IdOfNodesOfEdges = []
   
   mesh = ExtAPI.DataModel.AnalysisList[0].MeshData   
   NodesIdsOfElement = []
   ElementOfFace = mesh.ElementById(IdOfElement)
   NodesIdOfElement =   ElementOfFace.CornerNodeIds
   

   for i in range(len(NodesIdOfElement)):
      # for   
      if i != len(NodesIdOfElement)-1:
         if CheckFreeFace(NodesIdOfElement[i],NodesIdOfElement[i+1]):
            licznik = 0
            for NodeOnCurve in NodesOnCurve:
               if NodeOnCurve == NodesIdOfElement[i]:
                  licznik += 1
                  if licznik == 2:
                     break
               if NodeOnCurve == NodesIdOfElement[i+1]:
                  licznik += 1
                  if licznik == 2:
                     break
            
            if licznik == 2:
               IndexOfEdges.append(i+1)
               IdOfNodesOfEdges.append(NodesIdOfElement[i])
               IdOfNodesOfEdges.append(NodesIdOfElement[i+1])               
      elif i == len(NodesIdOfElement)-1:
      # for last edge of element
         if CheckFreeFace(NodesIdOfElement[i],NodesIdOfElement[0]):
            licznik = 0
            for NodeOnCurve in NodesOnCurve:
               if NodeOnCurve == NodesIdOfElement[i]:
                  licznik += 1
                  if licznik == 2:
                     break
               if NodeOnCurve == NodesIdOfElement[0]:
                  licznik += 1
                  if licznik == 2:
                     break
            
            if licznik == 2:
               IndexOfEdges.append(4)
               IdOfNodesOfEdges.append(NodesIdOfElement[i])
               IdOfNodesOfEdges.append(NodesIdOfElement[0])               
   return IndexOfEdges, IdOfNodesOfEdges


########################################################################################################
########################################################################################################
########################################################################################################

def CheckFreeFace(node1Id,node2Id):

   ElementsContainingNode1 = []
   ElementsContainingNode2 = []
   
   mesh = ExtAPI.DataModel.AnalysisList[0].MeshData

   ElementsContainingNode1 = mesh.NodeById(node1Id).ConnectedElementIds
   ElementsContainingNode2 = mesh.NodeById(node2Id).ConnectedElementIds
   
   NumberOfCommonElements = 0
   for ElmNode1 in ElementsContainingNode1:
   	for ElmNode2 in ElementsContainingNode2:
   	   if ElmNode1 == ElmNode2:
   	      NumberOfCommonElements += 1
   	      
   	      if NumberOfCommonElements > 1:
   	         break
   	if NumberOfCommonElements > 1:
   	   break
   
   if NumberOfCommonElements > 1:
      return False
   elif NumberOfCommonElements == 1:
      return True
   	      
########################################################################################################
########################################################################################################
########################################################################################################

def GetNodes(propGeo,Dimenions):

   PointsWhereToInterpolateIns = []

   if propGeo.Value:
      geoType = propGeo.Properties['DefineBy'].Value
      if geoType == 'Named Selection':
   	   refIds = propGeo.Value.Name
      else:
   	   refIds = propGeo.Value.Ids
           
      # Get the mesh of the model
      mesh = ExtAPI.DataModel.AnalysisList[0].MeshData
      # Loop on the list of the selected face id
      for refId in refIds:
  	   # Get mesh information for each face
   	   meshRegion = mesh.MeshRegionById(refId)
   	   IdOfNodes = meshRegion.NodeIds   
   				
	   for IdOfNode in IdOfNodes:
	      # Get internal objcet "Node" by its id??
	      NodeOfFace = mesh.NodeById(IdOfNode)		
       	      if Dimenions == 2:
         	PointsWhereToInterpolateIns.append(Point2d(IdOfNode,NodeOfFace.X,NodeOfFace.Y))
              elif Dimenions == 3:
         	PointsWhereToInterpolateIns.append(Point3d(IdOfNode,NodeOfFace.X,NodeOfFace.Y,NodeOfFace.Z))
         	
   	
   return PointsWhereToInterpolateIns 
      
########################################################################################################
########################################################################################################
########################################################################################################
        
class ElementWithEdge2d(Point2d):
#  Element name -> Id
#  Element Center 
    def __init__(self,ElmId,FaceIdex,Node1Id,Node2Id,CenterPoint):
        
        self.ElmId = ElmId
        self.FaceIdex = FaceIdex
        self.Node1Id = Node1Id
        self.Node2Id = Node2Id
        self.CenterPoint = CenterPoint
    
########################################################################################################
        
class ElementWithFace3d(ElementWithEdge2d):
#  Element name -> Id
#  Element Center 
    def __init__(self,ElmId,FaceIdex,Node1Id,Node2Id,Node3Id,Node4Id,CenterPoint):
        
        ElementWithEdge2d.__init__(self,ElmId,FaceIdex,Node1Id,Node2Id,CenterPoint)
        self.Node3Id = Node3Id
        self.Node4Id = Node4Id
        
########################################################################################################
########################################################################################################
########################################################################################################        








