
from pyexpat.errors import codes
from math import pi, cos, sin, sqrt,atan, tan,atan2,acos
import FreeCAD as App
import Draft
import os
from Astorlab_Functions import getRadius 

  
doc = App.activeDocument()

rads =  getRadius()
radius = rads[0]
if radius < 50.0 :
    print("Radius is too small")
    exit

Rad1 = rads[1]
Rcap = radius*0.8642 
Rmain = Rcap/1.5235131707
Rcan = Rmain*0.6563776535

axis = App.Vector(0, 0, 1)

try:     
	       
    #Outer Circle
    circle = Draft.make_circle(Rad1,  face=False)

    #Capricorn circle
    circle = Draft.make_circle(Rcap,  face=False)

    #Pin circle
    circle = Draft.make_circle(2.0,  face=False)

    #Ecliptic circle
    eclipRad = Rmain*1.0899454121    
    yd =  Rmain*0.4335677586
    center = App.Placement(App.Vector(0,yd, 0), App.Rotation(axis, 0))   
    circle = Draft.make_circle(eclipRad, placement=center ,  face=False)
    circle.ViewObject.LineColor =  (1.0,0.0,0.0)

    #Ecliptic Inner circle
    reclipIn = eclipRad*0.828683
    circle = Draft.make_circle(reclipIn, placement=center ,  face=False)
    circle.ViewObject.LineColor =  (0.0,0.0,1.0)
    
    d= eclipRad - reclipIn
    dh = d/2
    dq = d/4

    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "Stars.txt")

    if(file_path != '') :   
        file = open(file_path,'r') 
        for line in file:
            list = line.rsplit() 
            y = Rmain*float(list[-1])
            x = Rmain*float(list[-2]) 
            center = App.Placement(App.Vector(x, y, 0.) , App.Rotation(axis, 0))             
            circle = Draft.make_circle(0.5, placement=center,  face=False)
            text = Draft.make_text(list[1], placement=App.Vector(x,y, 0.)) 
            text.ViewObject.FontSize = 2.5 

    file.close()


    for alfa in range(0,361):

        ralfa = (alfa+90.0)*pi/180.0
        sina = sin(ralfa)
        sina2 = sina*sina
        cosb = (yd*sina2 + cos(ralfa)*sqrt(eclipRad*eclipRad-yd*yd*sina2))/eclipRad
        y = yd - eclipRad*cosb
        beta = acos(cosb)       
        x = eclipRad*sin(beta)
        if(alfa > 90 and alfa <= 270) :
            x = -x
        if (alfa % 5 == 0 and alfa % 30 != 0) :
            dt = dh
        elif(alfa % 30 == 0) :
            dt = d
        else :
            dt = dq    
       
        y1 = y + dt*cos(ralfa)
        x1 = x-dt*sin(ralfa) #r*sina
                     
        line = Draft.make_line(App.Vector(x, y, 0), App.Vector(x1, y1, 0))        
            
        if (alfa % 10 == 0 and alfa % 30 != 0) : 
            n = int(abs(alfa) / 30)
            num = abs((abs(alfa)-n*30)/10 )
            if (num % 2 == 0 ) :  
                day = "20"   
            else :
                day = "10"     
            text = Draft.make_text(day, placement=App.Vector(x1,y1, 0.)) 
            text.ViewObject.FontSize = 1  
      
                    
    line = Draft.make_line(App.Vector(-Rad1, 0, 0), App.Vector(Rad1, 0, 0))
    line.ViewObject.LineColor =  (1.0,0.0,0.0)
    line.ViewObject.DrawStyle = u"Dashdot"
    line = Draft.make_line(App.Vector(0, Rad1, 0), App.Vector(0, -Rad1, 0))   
    line.ViewObject.LineColor =  (1.0,0.0,0.0)
    line.ViewObject.DrawStyle = u"Dashdot"

    doc.recompute()
except IOError :
        print('Error in reading file')  
        file.close()

