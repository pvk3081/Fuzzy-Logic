# -*- coding: utf-8 -*-
"""
Created on Sat Nov 16 11:54:03 2019

@author: ASUS
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 18:30:14 2019

@author: ASUS
"""

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import pylab
import cv2
from PIL import Image
import time 

class Car:
    def __init__(self,i,Vmax,newdesx,newdesy,ObsDist,view,accl,acco):
        self.id=i
        self.Vmax = Vmax #20
        self.ObsDist = ObsDist
        self.VCntrl1,self.VCntrl2 = self.CreateEngine(view=view,accl= accl,acco=acco)
        self.newdesx = newdesx
        self.newdesy = newdesy
    
    def CreateEngine(self,DestDiv=3,VDiv=3,VdestDiv=5,view=1,accl=3,acco=5):
        '''******* Input  Fuzzification *********'''
        Destx = ctrl.Antecedent(np.arange(0,1+0.0001, 0.001), 'Destx')
        Destx.automf(DestDiv)
        if view==1:    
            Destx.view()
            
        Desty = ctrl.Antecedent(np.arange(0,1+0.0001, 0.001), 'Desty')
        Desty.automf(DestDiv)
        if view==1:    
            Desty.view()
       
        Vx = ctrl.Antecedent(np.arange(0, 1+0.001, 0.01), 'Vx')
        Vx.automf(VDiv)
        if view==1:
           Vx.view()
           
        Vy = ctrl.Antecedent(np.arange(0, 1+0.001, 0.01), 'Vy')
        Vy.automf(VDiv)
        if view==1:
           Vy.view()

        Dobsx = ctrl.Antecedent(np.arange(0,1+0.0001, 0.001), 'Dobsx')
        Dobsx.automf(DestDiv)
        if view==1:    
            Dobsx.view()
            
        Dobsy = ctrl.Antecedent(np.arange(0,1+0.0001, 0.001), 'Dobsy')
        Dobsy.automf(DestDiv)
        if view==1:    
            Dobsy.view()
       
        '''********Output Fuzzification***********'''
        Vdestx = ctrl.Consequent(np.arange(-accl-0.001, accl+0.001, 0.1), 'Vdestx')
#        Vdest = ctrl.Consequent(np.arange(0-0.001, 1+0.001, 0.1), 'Vdest')
        Vdestx.automf(VdestDiv)
        
        Vdesty = ctrl.Consequent(np.arange(-accl-0.001, accl+0.001, 0.1), 'Vdesty')
#        Vdest = ctrl.Consequent(np.arange(0-0.001, 1+0.001, 0.1), 'Vdest')
        Vdesty.automf(VdestDiv)

        Vobsx = ctrl.Consequent(np.arange(-acco-0.001, int(acco/2)+0.001, 0.1), 'Vobsx')
#        Vdest = ctrl.Consequent(np.arange(0-0.001, 1+0.001, 0.1), 'Vdest')
        Vobsx.automf(VdestDiv)
        
        Vobsy = ctrl.Consequent(np.arange(-acco-0.001, int(acco/2)+0.001, 0.1), 'Vobsy')
#        Vdest = ctrl.Consequent(np.arange(0-0.001, 1+0.001, 0.1), 'Vdest')
        Vobsy.automf(VdestDiv)
       
        if view==1:
            Vdestx.view()
            Vdesty.view()
            Vobsx.view()
            Vobsy.view()
       
        '''
        V
        s poor m average f good
         
        Dest
        close poor m average far good
       
        Vdest
        s poor m average f good
       
        '''
       
        ''' ***********Inference Rules**************   '''
        rule1 = ctrl.Rule(Vx['poor'] & Destx['poor'] | Vx['average'] & Destx['average'] , Vdestx['average'])
        
        rule2 = ctrl.Rule(Vy['poor'] & Desty['poor'] | Vy['average'] & Desty['average'] , Vdesty['average'])
       
        rule3 = ctrl.Rule(Vx['poor'] & Destx['average'] | Vx['poor'] & Destx['good'] | Vx['average'] & Destx['good']
                            , Vdestx['decent'])
        
        rule4 = ctrl.Rule(Vy['poor'] & Desty['average'] | Vy['poor'] & Desty['good'] | Vy['average'] & Desty['good']
                            , Vdesty['decent'])
        
        rule5 = ctrl.Rule(Vx['average'] & Destx['poor'] | Vx['good'] & Destx['average'] , Vdestx['mediocre'])
        
        rule6 = ctrl.Rule(Vy['average'] & Desty['poor'] | Vy['good'] & Desty['average'] , Vdesty['mediocre'])
       
       
        rule7 = ctrl.Rule(Vx['good'] & Destx['good'], Vdestx['good'])
        
        rule8 = ctrl.Rule(Vy['good'] & Desty['good'], Vdesty['good'])

        rule9 = ctrl.Rule(Vx['good'] & Destx['poor'], Vdestx['poor'])
        
        rule10 = ctrl.Rule(Vy['good'] & Desty['poor'], Vdesty['poor']) 

        rule11 = ctrl.Rule(Vx['poor'] & Dobsx['poor'] | Vx['average'] & Dobsx['average'] , Vobsx['average'])
        
        rule12 = ctrl.Rule(Vy['poor'] & Dobsy['poor'] | Vy['average'] & Dobsy['average'] , Vobsy['average'])
       
        rule13 = ctrl.Rule(Vx['poor'] & Dobsx['average'] | Vx['poor'] & Dobsx['good'] | Vx['average'] & Dobsx['good']
                            , Vobsx['decent'])
        
        rule14 = ctrl.Rule(Vy['poor'] & Dobsy['average'] | Vy['poor'] & Dobsy['good'] | Vy['average'] & Dobsy['good']
                            , Vobsy['decent'])
         
        rule15 = ctrl.Rule(Vx['average'] & Dobsx['poor'] | Vx['good'] & Dobsx['average'] , Vobsx['mediocre'])
        
        rule16 = ctrl.Rule(Vy['average'] & Dobsy['poor'] | Vy['good'] & Dobsy['average'] , Vobsy['mediocre'])
       
        rule17 = ctrl.Rule(Vx['good'] & Dobsx['good'], Vobsx['good'])
        
        rule18 = ctrl.Rule(Vy['good'] & Dobsy['good'], Vobsy['good'])

        rule19 = ctrl.Rule(Vx['good'] & Destx['poor'], Vobsx['poor'])
        
        rule20 = ctrl.Rule(Vy['good'] & Desty['poor'], Vobsy['poor'])


         
        #rule1.view()
       
        VelControlLong1 = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5,rule6, rule7, rule8, rule9, rule10])
        VelControlLong2 = ctrl.ControlSystem([rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18, rule19, rule20])
       
        VCntrl1 = ctrl.ControlSystemSimulation(VelControlLong1)
        VCntrl2 = ctrl.ControlSystemSimulation(VelControlLong2)
       
        return VCntrl1,VCntrl2

    def Move(self,DestDistx,DestDisty,vprevx,vprevy,prevdesx,prevdesy,countx,county,obs):
        velx = vprevx/self.Vmax
        vely = vprevy/self.Vmax
        flag7=0
        flag8=0
        if DestDistx ==0:  
            errx = 0
            print('dest x dist : ', 0)
            flag7=1
        if DestDisty == 0:
            erry = 0
            print('dest y dist : ', 0)
            flag8=1
        if flag7 == 0:
            errx = (DestDistx - prevdesx)/DestDistx
            print('dest x dist : ', (prevdesx)/DestDistx)
        if flag8 == 0:
            erry = (DestDisty - prevdesy)/DestDisty
            print('dest y dist : ', (prevdesy)/DestDisty)
        print("velx",velx)
        print("vely",vely)
        print("err",errx)
        print("err",erry)
   
        self.VCntrl1.input['Vx'] = velx
        self.VCntrl1.input['Vy'] = vely
        self.VCntrl1.input['Destx'] = errx
        self.VCntrl1.input['Desty'] = erry
  
        
     
        self.VCntrl1.compute()
       
        vn=vs=0
        vshortx = 0
        vshorty = 0
        vlongx = 0
        vlongy = 0
        flag3 = 0
        flag4 = 0
        vn=0
        vn1=0
        vs=0
        vs1=0
        
        if obs['N']!=None and obs['E']!=None:
        #if obs['N']!=None or obs['S']!=None or obs['E']!=None or obs['W']!=None:
        
            if obs['N']!=None:
                flag3 = 1
                self.VCntrl2.input['Vx'] = velx
                self.VCntrl2.input['Dobsx'] =(self.ObsDist-obs['N'])/self.ObsDist
                print("Dobsx",(self.ObsDist-obs['N'])/self.ObsDist)
                
            if obs['E']!=None:
                flag3=1
                self.VCntrl2.input['Vy'] = vely
                self.VCntrl2.input['Dobsy'] =(self.ObsDist-obs['E'])/self.ObsDist
                print("Dobsy",(self.ObsDist-obs['E'])/self.ObsDist)
                self.VCntrl2.compute()
                vn=self.VCntrl2.output['Vobsx']
                print("vn",vn)
                print('N dist : ', (obs['N'])/self.ObsDist)
                vn1=self.VCntrl2.output['Vobsy']
                print("vn",vn1)
                print('E dist : ', (obs['E'])/self.ObsDist)
          
        if obs['S']!=None and obs['W']!=None:
            if obs['S']!=None:
                flag4 = 1
                self.VCntrl2.input['Vx'] = velx
                self.VCntrl2.input['Dobsx'] = (self.ObsDist-obs['S'])/self.ObsDist
                print("Dobsx",(self.ObsDist-obs['S'])/self.ObsDist)
                
            if obs['W']!=None:
                    self.VCntrl2.input['Vy'] = vely
                    self.VCntrl2.input['Dobsy'] = (self.ObsDist-obs['W'])/self.ObsDist
                    print("Dobsy",(self.ObsDist-obs['W'])/self.ObsDist)
                    self.VCntrl2.compute()
                    vs=self.VCntrl2.output['Vobsx']
                    vs=vs*-1
                    print("vs",vs)
                    print('S dist : ', (obs['S'])/self.ObsDist)
                    vs1=self.VCntrl2.output['Vobsy']
                    vs1=vs1*-1
                    print("vs",vs1)
                    print('W dist : ', (obs['W'])/self.ObsDist)
                    
                
            print("vs",vs)
            if vn >0 and vs>0:
                vshortx = (vn + vs)/2                        
            else:
                vshortx = vn + vs
                
        
            if vn1 >0 and vs1>0:
                vshorty = (vn1 + vs1)/2                        
            else:
                vshorty = vn1 + vs1
          
        else:    
           vlongx = self.VCntrl1.output['Vdestx']
           vlongy = self.VCntrl1.output['Vdesty']
        
        
        
        vnewx = vprevx + vlongx + vshortx
        vnewy = vprevy + vlongy + vshorty
        print("vnewx",vnewx)
        print("vnewx",vnewy)
#        print(self.id,vshort,vlong,vnew,prevdes)
        if vnewx>=self.Vmax :
            vnewx = self.Vmax
        if vnewy>=self.Vmax :
            vnewy = self.Vmax
        if vnewx<=0 :
            vnewx = 0
        if vnewy<=0 :
            vnewy = 0
           
    #    if (vnew-vprev)==0:
    #        tempdes = 0
    #    else:
    #        tempdes = (vnew**2 - vprev**2)/(2*(vnew-vprev))
        tempdesx = vnewx
        tempdesy = vnewy
        newdesx = prevdesx + tempdesx
        newdesy = prevdesy + tempdesy
        print("newdesx",newdesx)
        print("newdesy",newdesy)
#        print('V : ',vnew,'   ','dest : ',newdes)
    #    Vdest.view(sim=VCntrl)
        if prevdesx - 0.1 < newdesx < prevdesx + 0.1:
            countx+=1
        else:
            countx=0
            
        if prevdesy - 0.1 < newdesy < prevdesy + 0.1:
            county+=1
        else:
            county=0
           
        if countx>=3 and county>=3:
            return vnewx,prevdesx,countx,vnewy,prevdesy,county,1
       
        self.newdesx = newdesx
        self.newdesy = newdesy
        return vnewx,newdesx,countx,vnewy,newdesy,county,0
    
    def GetObstacle(self,cars,newdesx,newdesy):
        d = {}
        d['N'] = None
        d['S'] = None
        d['E'] = None
        d['W'] = None
        for car in cars:
           dist1 = car.newdesx - newdesx
           dist2 = car.newdesy - newdesy
           print("car.newdesx",car.newdesx)
           print("car.newdesy",car.newdesy)
           print("newdesx",newdesx)
           print("newdesy",newdesy)
           print("dist1",dist1)
           print("dist2",dist2)
           if dist1>0:
               if dist1<=self.ObsDist:
                   d['N'] = dist1

           elif dist1<0:
               if abs(dist1)<=self.ObsDist:
                   d['S'] = abs(dist1)             
                   
           if dist2>0:
               if dist2<=self.ObsDist:
                   d['E'] = dist2

           elif dist2<0:
               if abs(dist2)<=self.ObsDist:
                   d['W'] = abs(dist2)
       
        print(d)
        return d
       
    
vnew2 = 0
prevdes2 = 0
newdes2=9
count2= 0
DestDist2 = 100
src1 = [0,0]
dest1 = [40,40]
src1x = src1[0]
src1y = src1[1]
src2 = [0,10]
dest2 = [40,40]
src2x = src2[0]
src2y = src2[1]
dest1x = dest1[0]
dest1y = dest1[1]
dest2x = dest2[0]
dest2y = dest2[1]

newdes5=src1x
newdes6=src1y
newdes7=src2x
newdes8=src2y


vnew1x = 0
vnew1y=0
vnew2x = 0
vnew2y=0
prevdes1 = 0
newdes1=0
newdes3=0
count1= 0
count3=0
count4=0
DestDist1 = 100 
c1 = Car(i=1,Vmax=10,newdesx=newdes5,newdesy=newdes6,ObsDist=10,view=0,accl=3,acco=5)
c2 = Car(i=2,Vmax=30,newdesx=newdes7,newdesy=newdes8,ObsDist=10,view=0,accl=4,acco=5)

print(c1.__dict__)
#print(c2.__dict__)

#cars = [c2]
#for car in cars:
#    print(car.__dict__)
flag1=0
flag2=0
cd1d = []
cd2d = []
cd1v = []
cd2v = []
cp1 = []
cp2 = []
i=0

print("newdes5",newdes5)
time.sleep(7)
while newdes5<dest1x or newdes6<dest1y or newdes7<dest2x or newdes8<dest2y :
    print("src1x",newdes5)
    print("src1y",newdes6)
    print("src2x",newdes7)
    print("src2y",newdes8)
    print("flag1",flag1)
    if newdes5<dest1x or newdes6<dest1y:
        
        if flag1==0:
            obs1 = c1.GetObstacle([c2],newdes5,newdes6)
            print("obs",obs1)
            vnew1,newdes5,count1,vnew2,newdes6,count2,flag1 = c1.Move(dest1x,dest1y,vnew1x,vnew1y,newdes5,newdes6,count1,count2,obs1)
            cd1v.append(vnew1)
            cd1d.append(newdes5)
            cp1.append(newdes6)
       # cp1.append(i)
   
#    print('V1 : ',vnew,'   ','dest1 : ',newdes)
    if newdes7<dest2x or newdes8<dest2y:
        if flag2 == 0:
            obs2 = c2.GetObstacle([c1],newdes7,newdes8)
            print("obs2",obs2)
            vnew3,newdes7,count3,vnew4,newdes8,count4,flag2 = c2.Move(dest2x,dest2y,vnew2x,vnew2y,newdes7,newdes8,count3,count4,obs2)
            cd2v.append(vnew3)
            cd2d.append(newdes7)
            cp2.append(newdes8)
            print("flag2",flag2)
#    print('V2 : ',vnew,'   ','dest2 : ',newdes)s
#    print('dest1 : ',newdes1,count1,'   ','dest2 : ',newdes2,count2)
    i+=1
    if flag1==1 and flag2==1:
        break
    
    
    env = np.zeros((50, 50, 3), dtype=np.uint8)
    env1 = np.zeros((50, 50, 3), dtype=np.uint8)
    env[int(newdes5)][int(newdes6)] = (255, 175, 0)
    env[int(newdes7)][int(newdes8)] = (255, 175, 0)
    env[int(dest2[0])][int(dest2[1])] = (0, 0, 255)
    img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img = img.resize((1000, 1000))  # resizing so we can see our agent in all its glory.
    img1 = Image.fromarray(env1, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
    img1 = img.resize((1000, 1000))  # resizing so we can see our agent in all its glory.
    cv2.imshow("image", np.array(img))  # show it!
   # cv2.imshow("image1", np.array(img1))  # show it!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.1)
#print("i",i)   
#pylab.clf()
#pylab.plot(cp1,cd1v,'-b',label = 'Car 1')-
#pylab.plot(cp2,cd2v,'-r',label = 'Car 2')
#pylab.show()

pylab.clf()
plt.plot(cd1d,cp1,'-g',label = 'Car 1')
plt.plot(cd2d,cp2,'-y',label = 'Car 2')
pylab.ylim([0,100])
pylab.xlim([0,100])
plt.xlabel('X-co-ordinate')
plt.ylabel('Y-co-ordinate')
plt.show()



#env = np.zeros((150, 150, 3), dtype=np.uint8)  # starts an rbg of our size
#env[int(newdes1)][int(newdes2)] = (255, 175, 0)  # sets the food location tile to green color
#img = Image.fromarray(env, 'RGB')  # reading to rgb. Apparently. Even tho color definitions are bgr. ???
#img = img.resize((1000, 1000))  # resizing so we can see our agent in all its glory.
#cv2.imshow("image", np.array(img))  # show it!
#if cv2.waitKey(1) & 0xFF == ord('q'):
#    cv2.destroyAllWindows()
#    time.sleep(1)