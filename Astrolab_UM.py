

from math import pi, cos, sin, sqrt,atan, tan,atan2,asin
import FreeCAD as App
import Draft
from PySide import QtGui
from Astorlab_Functions import getRadius , tickLines_1 , Korsi

doc = App.activeDocument()

    
# *****************************************************


rads =  getRadius()
radius = rads[0]
if radius < 50.0 :
    print("Radius is too small")
    exit

Rad1 = rads[1]


#Outside circle
circle = Draft.make_circle(radius,  face=False)

#Inside circle
circle = Draft.make_circle(Rad1,  face=False)

#Pin circle
circle = Draft.make_circle(2.0,  face=False)

Korsi(radius)
tickLines_1(radius,Rad1, 0,360,1)
       
line = Draft.make_line(App.Vector(0, Rad1, 0), App.Vector(0, -Rad1, 0))
line.ViewObject.LineColor =  (1.0,0.0,0.0)
line.ViewObject.DrawStyle = u"Dashdot"
line = Draft.make_line(App.Vector(Rad1, 0, 0), App.Vector(-Rad1, 0, 0))
line.ViewObject.LineColor =  (1.0,0.0,0.0)
line.ViewObject.DrawStyle = u"Dashdot"

doc.recompute()

