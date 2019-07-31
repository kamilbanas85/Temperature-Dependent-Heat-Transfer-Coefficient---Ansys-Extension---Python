from POINT__Lib import *

########################################################################################################
########################################################################################################
########################################################################################################

def WriteDataToFile(FileName,Label,*args):
    
    f = open(FileName, "w")
    
    if (Label):
        for Lab in Label:
            f.write("{:>16}  ".format(Lab))
        f.write("\n")

    for i,x in enumerate(args[0]):
        for arg in args:
            if (type (arg[i]) is int):
                f.write("{:16d}  ".format(arg[i]))
            else:
                f.write("{:16.6f}  ".format(arg[i]))
        f.write("\n")
    f.close()
 

########################################################################################################
########################################################################################################
########################################################################################################


def AppendDataToFile(FileName,Label,*args):
    
    f = open(FileName, "r")
    lines = f.readlines()
    f.close()
    
    f = open(FileName, "w")
    
    for i,line in enumerate(lines):
        f.write("{}".format(line.strip("\n")))
        
        if (i==0 and Label):
            for Lab in Label:
                f.write("{:>16}  ".format(Lab))
        elif (i>0 and Label):
           for arg in args:
              if (type (arg[i-1]) is int):
                  f.write("{:10d}  ".format(arg[i-1]))
              else:
                  f.write("{:16.6f}  ".format(arg[i-1]))
        elif (Label == None ):
            for arg in args:
                if (type (arg[i]) is int):
                    f.write("{:16d}  ".format(arg[i]))
                else:
                    f.write("{:10.8f}  ".format(arg[i])) 
        f.write("\n")    
    f.close()       

########################################################################################################
########################################################################################################
########################################################################################################

def ReadDataFLUENT(FileName,Dimenions):

   Points = []
   Temp = []
   HeatFlux =[]

   TxtFile = open(FileName, 'r')

   lines = TxtFile.readlines()[1:]
   for line in lines:
      a=line.split(',')
      if Dimenions == 2:
         Points.append(Point2d(int(a[0]),float(a[1]),float(a[2])))
	 Temp.append(float(a[3]))
	 HeatFlux.append(float(a[4]))
      elif Dimenions == 3:
	 Points.append(Point3d(int(a[0]),float(a[1]),float(a[2]),float(a[3])))
	 Temp.append(float(a[4]))
	 HeatFlux.append(float(a[5]))
    
   TxtFile.close()
    
   return Points, Temp, HeatFlux
