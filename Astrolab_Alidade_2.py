

from math import pi, cos
import FreeCAD as App
import Part
import Draft
from Astorlab_Functions import  getRadius 

doc = App.activeDocument()

rads =  getRadius()
radius = rads[0]
if radius < 50.0 :
    print("Radius is too small")
    exit

Rad1 = rads[1]

center = App.Vector(0, 0, 0)
axis = App.Vector(0, 0, 1)


#Pin circle
circle = Part.Circle(center, axis, 2.0)
obj = doc.addObject("Part::Feature", "Circle")
obj.Shape = circle.toShape()

y = 10.0
x = Rad1 - y
cos45 = cos(pi/4.0) 
y2 = y*cos45
x2 =  y2 
h = 10 

p1 = App.Vector(-h, 0., 0.)   
p2 = App.Vector(-x2,y2, 0.)
p3 = App.Vector(0.0,h, 0.)
arc2 = Part.Arc(p1, p2, p3)
obj = doc.addObject("Part::Feature", "Arc")
obj.Shape = arc2.toShape()

p1 = App.Vector(h, 0., 0.)   
p2 = App.Vector(x2,-y2, 0.)
p3 = App.Vector(0.0,-h, 0.)
arc2 = Part.Arc(p1, p2, p3)
obj = doc.addObject("Part::Feature", "Arc")
obj.Shape = arc2.toShape()
   
line = Draft.make_line(App.Vector(-Rad1, 0., 0.), App.Vector(-h, 0., 0.))
line = Draft.make_line(App.Vector(h, 0., 0.), App.Vector(Rad1, 0., 0.))

line = Draft.make_line(App.Vector(-Rad1+h, -h, 0.), App.Vector(0.0, -h, 0.))
line = Draft.make_line(App.Vector(0.0, h, 0.), App.Vector(Rad1-h, h, 0.))

pl = App.Vector(-x+10.0,-7, 0.)  
rec = Draft.makeRectangle(3.0, 7.)  
Draft.move(rec, pl)
pl = App.Vector(x-10,0.0, 0.) 
rec = Draft.makeRectangle(3.0, 7.)  
Draft.move(rec, pl)  

p1 = App.Vector(-x, -y, 0.)  
p2 = App.Vector(-x - x2,-y2, 0.)
p3 = App.Vector(-Rad1,0., 0.)
arc2 = Part.Arc(p1, p2, p3)
obj = doc.addObject("Part::Feature", "Arc")
obj.Shape = arc2.toShape()

p1 = App.Vector(x, y, 0.)    
p2 = App.Vector(x + x2,y2, 0.)
p3 = App.Vector(Rad1,0., 0.)
arc2 = Part.Arc(p1, p2, p3)
obj = doc.addObject("Part::Feature", "Arc")
obj.Shape = arc2.toShape()


doc.recompute()

