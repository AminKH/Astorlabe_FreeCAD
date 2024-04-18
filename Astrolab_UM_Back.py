

from math import pi, cos, sin, sqrt,atan, tan,atan2,asin
import FreeCAD as App
import Part
import Draft
from Astorlab_Functions import  getRadius , tickLines_1 ,  sincosLines , Korsi

doc = App.activeDocument()

def tickLines_2(Side,Radi, start,end,step): 

    pl=App.Placement()
    pl.Rotation.Q=(0.0, 0.0, 0.0, 1.0)      	
        
    for angle in range(start,end,step):  
        writeText = False         
        lineColor = (0.0,0.0,0.0)                
        
        radIn = Radi - 2.0
        rangle = atan(-angle/100.0)
        if(Side == "Up") :
            rangle = rangle - pi/2.0
        
        if(angle%5 == 0 and angle%10 != 0) :
            writeText = True
            lineColor = (0.00,0.00,1.00)                  
            radIn = Radi - 4.0              
            radText = radIn                             
        elif(angle%5 == 0 and angle%10 == 0) :
            writeText = True
            lineColor = (1.00,0.00,0.00)                
            radIn = Radi - 6.0              
            radText = radIn    
        x1 = radIn*cos(rangle)
        y1 = radIn*sin(rangle)
        x2 = Radi*cos(rangle)
        y2 = Radi*sin(rangle)

        if(Side == "Right"):
            points = [App.Vector(x1, y1, 0.0), App.Vector(x2, y2, 0.0)]
        elif (Side=="Left"):
            points = [App.Vector(-x1, y1, 0.0), App.Vector(-x2, y2, 0.0)]
        line = Draft.makeWire(points, placement=pl, closed=False, face=False, support=None)
        line.ViewObject.LineColor =  lineColor
        line.ViewObject.DrawStyle = u"Solid"
        Draft.autogroup(line) 
        if(writeText == True) :           
            x3 = radText*cos(rangle)
            y3 = radText*sin(rangle)
            d =  angle 	
            if(Side=="Left") : 			
                text = Draft.make_text(str(abs(d)), placement=App.Vector(-x3,y3, 0.0))
            elif(Side=="Right"):
                text = Draft.make_text(str(abs(d)), placement=App.Vector(x3,y3, 0.0))
            text.ViewObject.FontSize = 0.75
            #Draft.autogroup(text)  


rads =  getRadius()
radius = rads[0]
if radius < 50.0 :
    print("Radius is too small")
    exit

Rad1 = rads[1]

center = App.Vector(0, 0, 0)
axis = App.Vector(0, 0, 1)

#Outside circle
circle = Part.Circle(center, axis, radius)
obj = doc.addObject("Part::Feature", "Circle")
obj.Shape = circle.toShape()

#Inside circle
circle = Part.Circle(center, axis, Rad1)
obj = doc.addObject("Part::Feature", "Circle")
obj.Shape = circle.toShape()

#Pin circle
circle = Part.Circle(center, axis, 2.0)
obj = doc.addObject("Part::Feature", "Circle")
obj.Shape = circle.toShape()

Korsi(radius)

tickLines_1(radius,Rad1, 0,360,1)

tickLines_2("Right",Rad1,0,80,1)
tickLines_2("Right",Rad1,80,200,5)
tickLines_2("Right",Rad1,200,260,10)
tickLines_2("Right",Rad1,300,1100,100)

tickLines_2("Left",Rad1,0,80,1)
tickLines_2("Left",Rad1,80,200,5)
tickLines_2("Left",Rad1,200,260,10)
tickLines_2("Left",Rad1,300,1100,100)

sincosLines(Rad1,2)
        
line = Draft.make_line(App.Vector(0, Rad1, 0), App.Vector(0, -Rad1, 0))
line.ViewObject.LineColor =  (1.0,0.0,0.0)
line.ViewObject.DrawStyle = u"Dashdot"
line = Draft.make_line(App.Vector(Rad1, 0, 0), App.Vector(-Rad1, 0, 0))
line.ViewObject.LineColor =  (1.0,0.0,0.0)
line.ViewObject.DrawStyle = u"Dashdot"

doc.recompute()

