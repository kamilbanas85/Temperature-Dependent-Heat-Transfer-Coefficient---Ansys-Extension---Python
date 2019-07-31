from POINT__Lib import *
from READ_WRITE__Lib import *

########################################################################################################
########################################################################################################
########################################################################################################

def Interpolate(PointsWhereToInterpolate,Path01,Path02,Path03,Dim,Method):


   BasePoints01,TempAtPoints01, HeatFluxAtPoints01 = ReadDataFLUENT(Path01,Dim)
   BasePoints02,TempAtPoints02, HeatFluxAtPoints02 = ReadDataFLUENT(Path02,Dim)
   	 	
   f1_HeatFlux = InterpolateNearestPoint(BasePoints01,HeatFluxAtPoints01)
   HeatFluxResults01 = f1_HeatFlux(PointsWhereToInterpolate)   
   f1_Temp = InterpolateNearestPoint(BasePoints01,TempAtPoints01)
   TempResults01 = f1_Temp(PointsWhereToInterpolate)
    
   f2_HeatFlux = InterpolateNearestPoint(BasePoints02,HeatFluxAtPoints02)
   HeatFluxResults02 = f2_HeatFlux(PointsWhereToInterpolate)   
   f2_Temp = InterpolateNearestPoint(BasePoints02,TempAtPoints02)
   TempResults02 = f2_Temp(PointsWhereToInterpolate)
   	   	
   if Method == "2 points":
   
      return HeatFluxResults01,HeatFluxResults02,TempResults01,TempResults02
      
   elif Method == "3 points":
   
      BasePoints03,TempAtPoints03,HeatFluxAtPoints03 = ReadDataFLUENT(Path03,Dim)

      f3_HeatFlux = InterpolateNearestPoint(BasePoints03,HeatFluxAtPoints03)
      HeatFluxResults03 = f3_HeatFlux(PointsWhereToInterpolate)      
      f3_Temp = InterpolateNearestPoint(BasePoints03,TempAtPoints03)
      TempResults03 = f3_Temp(PointsWhereToInterpolate)
      
      return HeatFluxResults01,HeatFluxResults02,HeatFluxResults03,TempResults01,TempResults02,TempResults03

########################################################################################################
########################################################################################################
########################################################################################################
	
class InterpolateNearestPoint(object):
    """
    Nearest point interpolation in 2 or 3 dimensions.
      
    BasePoints - list of points 2d or 3d 
    FuncValeAtPoints - list of function value at BasePoints
    PointsWhereToInterpolate - list of points 2d or 3d
    
    EXAMPLE of use
    
    f = InterpolateNearestPoint(BasePoints,FuncValeAtPoints)
    Results = f(PointsWhereToInterpolate)
    """
    
    def __init__(self,BasePoints,FuncValeAtPoints):
        self.BasePoints = BasePoints
        self.FuncValeAtPoints = FuncValeAtPoints
        
    def __call__(self, PointsWhereToInterpolate):
        """
        Evaluate interpolator at given points.
        PointsWhereToInterpolate list of points 2d or 3d 
        """
        Results = []
        
        for Point in PointsWhereToInterpolate:
            distanceTemp = 0
            SmallestDistance = 0
            i = 0
            for i, BasePoint in enumerate(self.BasePoints):
                distanceTemp = Point.Distance(BasePoint)
                if i==0:
                    SmallestDistance = distanceTemp
                    ResultTemp = self.FuncValeAtPoints[i]
                else:
                    if distanceTemp <= SmallestDistance:
                        SmallestDistance = distanceTemp
                        ResultTemp = self.FuncValeAtPoints[i]
                                    
            Results.append(ResultTemp)                     
            
        return Results