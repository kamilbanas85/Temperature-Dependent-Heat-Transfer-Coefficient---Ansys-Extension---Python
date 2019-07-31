class Point2d(object):
#         2 dimensions point -> name = id    
    def __init__(self,name,x,y):
    	self.name = name
        self.x = x
        self.y = y
        
    def Distance(self,Point2):
        dist = ( (self.x-Point2.x)**2 + (self.y-Point2.y)**2 )**0.5
        return dist
        
########################################################################################################
########################################################################################################
########################################################################################################
        
class Point3d(Point2d):
#        3 dimensions point
    def __init__(self,name,x,y,z):
        Point2d.__init__(self,name,x,y)
        self.z = z
        
    def DistansOfPoints(self,Point2):
        dist = ( (self.x-Point2.x)**2 + (self.y-Point2.y)**2 
                + (self.z-Point2.z)**2)**0.5
        return dist   
        
        
#### SORTOWANIE       
#### PointsWhereToInterpolate =  sorted(PointsWhereToInterpolate, key=lambda Point: Point.x)    
