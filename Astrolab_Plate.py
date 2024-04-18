

from math import pi, cos, sin, sqrt, tan,acos
import FreeCAD as App
import Draft
from PySide import QtGui, QtCore

class SelectItemsClass(QtGui.QDialog):
	""""""
	def __init__(self):
		super(SelectItemsClass, self).__init__()
		self.initUI()
	def initUI(self):
		self.result = userCancelled
		# create our window
		# define window		xLoc,yLoc,xDim,yDim
		self.setGeometry(	250, 250, 400, 220)
		self.setWindowTitle("Astorlab, Loction and Size ")
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		# create some Labels
		self.label1 = QtGui.QLabel("Please Enter Latitude of location", self)
		self.label1.setFont('Courier') # set to a non-proportional font
		self.label1.move(20, 20)  

		self.label2 = QtGui.QLabel("From 00.0000 to 90.0000 degrees", self)
		self.label2.setFont('Courier') # set to a non-proportional font
		self.label2.move(20, 35)   
	        
		self.label3 = QtGui.QLabel("Please Enter outer radius of Astrolab ", self)
		self.label3.setFont('Courier')
		self.label3.move(20, 65)		
	
		self.label4 = QtGui.QLabel("in milimeter. The same size as spider ", self)
		self.label4.setFont('Courier')
		self.label4.move(20, 80)
		
		self.label5 = QtGui.QLabel("Minimum radius is 50.0000 milimeters ", self)
		self.label5.setFont('Courier')
		self.label5.move(20, 95)
             
        # numeric input field
		self.numericInput1 = QtGui.QLineEdit(self)
		self.numericInput1.setInputMask("90.0000")
		self.numericInput1.setText("00.0000")
		self.numericInput1.setFixedWidth(50)
		self.numericInput1.move(320, 35)
		
        # numeric input field 
		self.numericInput2 = QtGui.QLineEdit(self)
		self.numericInput2.setInputMask("999.9999")
		self.numericInput2.setText("000.0000")
		self.numericInput2.setFixedWidth(60)
		self.numericInput2.move(320, 95)
            
		self.label5 = QtGui.QLabel("Select Altitude increment angle. ", self)
		self.label5.setFont('Courier')
		self.label5.move(20, 130)
  
        # set up lists for pop-ups
		self.popupItems1 = ("1","3","5","10","15")
        # set up pop-up menu
		self.popup1 = QtGui.QComboBox(self)
		self.popup1.addItems(self.popupItems1)
		self.popup1.setCurrentIndex(self.popupItems1.index("5"))
		self.popup1.activated[str].connect(self.onPopup1)
		self.popup1.move(320, 130)
		
		# cancel button
		cancelButton = QtGui.QPushButton('Cancel', self)
		cancelButton.clicked.connect(self.onCancel)
		cancelButton.setAutoDefault(True)
		cancelButton.move(120, 175)
		# OK button
		okButton = QtGui.QPushButton('OK', self)
		okButton.clicked.connect(self.onOk)
		okButton.move(230, 175)
		# now make the window visible
		self.show()
		#
		self.numericInput3 = QtGui.QLineEdit(self)
		self.numericInput3.setText("5")             
	def onPopup1(self, selectedText):	
		self.numericInput3.setText(selectedText) 
                  
	def onCancel(self):
		self.result			= userCancelled
		self.close()
	def onOk(self):
		self.result			= userOK
		self.close()
	
			
# Class definitions

# Function definitions

# Constant definitions
userCancelled = "Cancelled"
userOK = "OK"

# code ***********************************************************************************


form = SelectItemsClass()
form.exec_()

if form.result==userCancelled:
	pass # steps to handle user clicking Cancel
if form.result==userOK:
	# steps to handle user clicking OK
	localVariable1 = form.numericInput1.text()
	print("Latitude = " , localVariable1)
	localVariable2 = form.numericInput2.text()
	print(" Radius of Astrolabe " , localVariable2)
	localVariable3 = form.numericInput3.text()
	print(" Altitude increment angle " , localVariable3)
	
var1 = float(localVariable1)
if var1 > 90.0 or var1 <0.0 :
      print("Latitude is out of limits")
      exit

var2 = float(localVariable2) 
if var2 <50.0 :
      print("Radius is too small ")
      exit

n = int(localVariable3)
if(n == 1):
      q = 10
elif( n == 3) :
      q = 6
else:
      q = 5

doc = App.activeDocument()

phi = float(localVariable1)*pi/180.0
phial = pi/2.0 - phi

radius = var2
Rad1 = radius*0.92
Rcap  = radius*0.8642 
Rmain = Rcap/1.5235131707
Rcan = Rmain*0.6563776535

#Inside circle
circle = Draft.make_circle(Rad1, face=False)

#Capricorn circle
circle = Draft.make_circle(Rcap, face=False)

#Main circle
circle = Draft.make_circle(Rmain, face=False)

#Cancer circle
circle = Draft.make_circle(Rcan,  face=False)

#Pin circle
circle = Draft.make_circle(2.0,  face=False)

axis = App.Vector(0, 0, 1)

for alt in range(0,90,n):
    ralt = alt*pi/180.0
    y1 = tan((pi-phi-ralt)/2.0)
    y2 = tan((-phi+ralt)/2.0)
    y0= Rmain*(y1+y2)/2
    r= Rmain*(y1-y2)/2
      
    if(y0+r>Rad1):       
        p = (Rad1+r+y0)/2
        h = 2*sqrt(p*(p-r)*(p-Rad1)*(p-y0))/y0
        y = sqrt(Rad1*Rad1-h*h)
        p1 = App.Vector(-h, y, 0)
        p2 = App.Vector(0, Rmain*y2, 0)
        p3 = App.Vector(h, y, 0)       
        arc = Draft.make_arc_3points([p1,p2,p3])
        arc.ViewObject.LineColor = (0,0,127) 
    else:
        y0= App.Vector(0.0,y0,0.0)
        center = App.Placement(y0 , App.Rotation(axis, 0))             
        circle = Draft.make_circle(r, placement=center,  face=False)
        circle.ViewObject.LineColor = (0,0,127) 
                
        if(alt % q == 0 ) :                       
            text = Draft.make_text(str(alt), placement=App.Vector(0.0,y1*Rmain, 0.0))
            text.ViewObject.FontSize = 0.5 

    if(alt % q == 0 ) :                       
            text = Draft.make_text(str(alt), placement=App.Vector(0.0,y2*Rmain, 0.0))
            text.ViewObject.FontSize = 0.5 


for alt in range(-6,-24,-6):
    
    ralt = alt*pi/180.0
    y1 = tan((pi-phi-ralt)/2.0)
    y2 = tan((-phi+ralt)/2.0)
    y0= Rmain*(y1+y2)/2
    r= Rmain*(y1-y2)/2
    p = (Rad1+r+y0)/2
    h = 2*sqrt(p*(p-r)*(p-Rad1)*(p-y0))/y0
    y = y0-sqrt(r*r-h*h)
    p1 = App.Vector(-h, y, 0)
    p2 = App.Vector(0, Rmain*y2, 0)
    p3 = App.Vector(h, y, 0)   
    arc = Draft.make_arc_3points([p1,p2,p3])   
    arc.ViewObject.LineColor = (0,0,255)     

ya = Rmain*cos(phi)/(1.0+sin(phi))
p2 = App.Vector(0, ya , 0)

# Horizon Circle
r0= Rmain/cos(phial)
y0= Rmain*tan(phial)

# First Perpendicular
y1= -Rmain*tan(phi)
r= Rmain/cos(phi)

dy = y0-y1
dy2 = dy*dy

djy2 = y1*y1

for beta in range(-90-int(phi)+n,90+int(phi),n):
    rbeta = beta*pi/180.0      
    x1 = r*tan(rbeta)
    r1 = r/cos(rbeta)
    x1_2 = x1*x1
  
    d = sqrt(x1_2+dy2)
    p = (r0+r1+d)/2   
    h = 2*sqrt(p*(p-r0)*(p-r1)*(p-d))/d
    a = sqrt(r1*r1-h*h) 
    x2 = x1*(a/d-1)
    y2 = y1+a*dy/d  

    xp1 = x2+h*dy/d
    yp1 = y2-h*x1/d 
    rad2 = sqrt(xp1*xp1+yp1*yp1)
    xp2 = x2-h*dy/d
    yp2 = y2+h*x1/d 
    rad1 = sqrt(xp2*xp2+yp2*yp2)

    if(rad1 > Rad1 or rad2 > Rad1) :

        d = sqrt(x1_2+djy2)
        p = (Rad1+r1+d)/2   
        h = 2*sqrt(p*(p-Rad1)*(p-r1)*(p-d))/d
        a = sqrt(r1*r1-h*h) 
        x2 = x1*(a/d-1)
        y2 = y1*(1-a/d) 
        if(rad1 > Rad1):
            xp2 =  x2+h*y1/d
            yp2 =  y2+h*x1/d  
        elif(rad2 > Rad1):
            xp1 =  x2-h*y1/d
            yp1 =  y2-h*x1/d

    p1 = App.Vector(xp2, yp2, 0)    
    p3 = App.Vector(xp1, yp1, 0)
    arc = Draft.make_arc_3points([p1,p2,p3])   
    arc.ViewObject.LineColor = (0,85,255)

    if(beta % q == 0 ) :                       
            text = Draft.make_text(str(beta+270), placement=App.Vector(xp1,yp1, 0.0))
            text.ViewObject.FontSize = 0.5 
            text = Draft.make_text(str(abs(beta-90)), placement=App.Vector(-xp1,yp1, 0.0))
            text.ViewObject.FontSize = 0.5 


p = (Rcap+r0+y0)/2 
h = 2*sqrt(p*(p-Rcap)*(p-r0)*(p-y0))/y0
Jangdif = acos(h/Rcap)/6
#print(6*Jangdif*180.0/pi)
p = (Rcan+r0+y0)/2 
h = 2*sqrt(p*(p-Rcan)*(p-r0)*(p-y0))/y0
Sangdif = acos(h/Rcan)/6
#print(6*Sangdif*180.0/pi)
R15 = 15.0*pi/180.0

# Hour Lines    
for angle in range(0,6):    
    rangle = pi/2-R15*angle
    cosa = cos(rangle)
    sina = sin(rangle)
    xh1 = Rcap*cosa
    yh1 = -Rcap*sina    
    xh2 = Rmain*cosa
    yh2 = -Rmain*sina
    p2 = App.Vector(xh2, yh2, 0)  
    line = Draft.make_line(App.Vector(xh1, yh1, 0), App.Vector(xh2, yh2, 0))
    line.ViewObject.LineColor =  (1.0,0.0,0.0)
    line = Draft.make_line(App.Vector(-xh1, yh1, 0), App.Vector(-xh2, yh2, 0))
    line.ViewObject.LineColor =  (1.0,0.0,0.0)

    if(angle != 0) :          
        rangle1 = rangle - Jangdif*angle
        cosa = cos(rangle1)
        sina = sin(rangle1)
        xh1 = Rcap*cosa
        yh1 = -Rcap*sina
        p1 = App.Vector(xh1, yh1, 0)    
        rangle3 = rangle + Sangdif*angle
        cosa = cos(rangle3)
        sina = sin(rangle3)
        xh3 = Rcan*cosa
        yh3 = -Rcan*sina
        p3 = App.Vector(xh3, yh3, 0)  
        arc = Draft.make_arc_3points([p1,p2,p3])   
              
        p1 = App.Vector(-xh1, yh1, 0)    
        p2 = App.Vector(-xh2, yh2, 0)
        p3 = App.Vector(-xh3, yh3, 0) 
        arc = Draft.make_arc_3points([p1,p2,p3])   
             
        
line1 = Draft.make_line(App.Vector(0, Rad1, 0), App.Vector(0, -Rad1, 0))
line1.ViewObject.LineColor =  (1.0,0.0,0.0)
line1.ViewObject.DrawStyle = u"Dashdot"
line1 = Draft.make_line(App.Vector(Rad1, 0, 0), App.Vector(-Rad1, 0, 0))
line1.ViewObject.LineColor =  (1.0,0.0,0.0)
line1.ViewObject.DrawStyle = u"Dashdot"

doc.recompute()

