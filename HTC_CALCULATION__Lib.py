from POINT__Lib import *

########################################################################################################
########################################################################################################
########################################################################################################

def PrepareHTC_3Points(Points,HeatFlux1,HeatFlux2,HeatFlux3,Temp1,Temp2,Temp3):
   
   H0 = []
   H1 = []
   TAW = []
   
   deltaM = []
   licznik = 0
   
   for i,Point in enumerate(Points):
      
      Mg = [[1,Temp1[i],Temp1[i]**2],
   	    [1,Temp2[i],Temp2[i]**2],
   	    [1,Temp3[i],Temp3[i]**2]]
   
      Mc1 = [[HeatFlux1[i],Temp1[i],Temp1[i]**2],
   	     [HeatFlux2[i],Temp2[i],Temp2[i]**2],
   	     [HeatFlux3[i],Temp3[i],Temp3[i]**2]]
   	   
      Mc2 = [[1,HeatFlux1[i],Temp1[i]**2],
   	     [1,HeatFlux2[i],Temp2[i]**2],
   	     [1,HeatFlux3[i],Temp3[i]**2]]
   
      Mc3 = [[1,Temp1[i],HeatFlux1[i]],
   	     [1,Temp2[i],HeatFlux2[i]],
   	     [1,Temp3[i],HeatFlux3[i]]]
   	       
      Wg  = det(Mg)
      Wc1 = det(Mc1)
      Wc2 = det(Mc2)
      Wc3 = det(Mc3)
   	       
      c1 = Wc1/Wg
      c2 = Wc2/Wg
      c3 = Wc3/Wg
   	
      delta = c2**2 - 4*c3*c1
            
      if delta >= 0:
      
      #  Taw1 = (-c2-sqrt(delta))/(2*c3)
         Taw = (-c2 + delta**0.5)/(2*c3)
         h1 = c3
         h0 = -c1/Taw
      
         H0.append(h0)
         H1.append(h1)
         TAW.append(Taw)     
         #
         deltaM.append(delta)
         #
         
      elif delta < 0:
   	 licznik += 1
   	 
         Taw = (-c2)/(2*c3)
         h1 = c3
         h0 = -c1/Taw
      
         H0.append(h0)
         H1.append(h1)
         TAW.append(Taw)  
         #
         deltaM.append(delta)
         #
   
   return H0,H1,TAW,deltaM,licznik

########################################################################################################
########################################################################################################
########################################################################################################

def PrepareHTC_2Points(Points,HeatFlux1,HeatFlux2,Temp1,Temp2):
   
   HTC2Points = []
   TAW2Points = []
   
   for i,Point in enumerate(Points):
      
      deltaHeatFlux = HeatFlux2[i] - HeatFlux1[i]
      deltaTemp = Temp2[i] - Temp1[i]
      
      htc = deltaHeatFlux/deltaTemp
      HTC2Points.append(htc)
      
      TempAvg = ( Temp2[i] + Temp1[i] )/2 
      HeatFluxAvg = ( HeatFlux2[i] + HeatFlux1[i] )/2 
      Taw = TempAvg + HeatFluxAvg/htc
      TAW2Points.append(Taw)
      
   
   return HTC2Points,TAW2Points
   
########################################################################################################
########################################################################################################
########################################################################################################

"http://code.activestate.com/recipes/578108-determinant-of-matrix-of-any-order/"
     
def det(l):
    n=len(l)
    if (n>2):
        i=1
        t=0
        sum=0
        while t<=n-1:
            d={}
            t1=1
            while t1<=n-1:
                m=0
                d[t1]=[]
                while m<=n-1:
                    if (m==t):
                        u=0
                    else:
                        d[t1].append(l[t1][m])
                    m+=1
                t1+=1
            l1=[d[x] for x in d]
            sum=sum+i*(l[0][t])*(det(l1))
            i=i*(-1)
            t+=1
        return sum
    else:
        return (l[0][0]*l[1][1]-l[0][1]*l[1][0])