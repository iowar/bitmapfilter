#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import sys
import numpy     as np
import itertools as itl
from PIL    import Image
from PySide import QtGui, QtCore

class IMG(QtGui.QLabel):


    click = QtCore.Signal(list)
    move  = QtCore.Signal(list)

    def __init__(self, parent=None):
	super(IMG, self).__init__(parent)
	
	self.pic = Image.open(IMGFILE)
	self.setPixmap(QtGui.QPixmap(IMGFILE))
	self.setFixedSize(self.pic.size[0],self.pic.size[1])
	self.setMouseTracking(True)

    ########### click slot ################
    def mousePressEvent(self, event):
        self.click.emit( [event.x(),event.y()] )

    ########### move slot ################
    def mouseMoveEvent(self,event):
	self.move.emit([ event.x(),event.y() ])

class Win(QtGui.QMainWindow):

    def __init__(self, parent=None):
	super(Win, self).__init__(parent)
	self.initUI()
	self.infoimg()
	self.FRGB = 5
	self.RATE = 128

    def initUI(self):
	self.widget   = QtGui.QWidget()
	self.hlayout  = QtGui.QHBoxLayout()
	self.vlayout  = QtGui.QVBoxLayout()
	self.h2layout = QtGui.QHBoxLayout()
	self.v2layout = QtGui.QVBoxLayout()
	
	############# RGB RATE SLIDE ##########
        self.rgb_rate = QtGui.QSlider(QtCore.Qt.Horizontal)
     	self.rgb_rate.setRange(0, 255)
      	self.rgb_rate.setValue(128)
     	self.rgb_rate.setEnabled(True)                                  
    	self.connect(self.rgb_rate, QtCore.SIGNAL("valueChanged(int)"),
   		    self._RATE)

	############# Selected R,G,B SLIDE ##########
        self.wrgb = QtGui.QSlider(QtCore.Qt.Horizontal)
     	self.wrgb.setRange(0, 5)
      	self.wrgb.setValue(5)
     	self.wrgb.setEnabled(True)                

    	self.connect(self.wrgb, QtCore.SIGNAL("valueChanged(int)"),
   		    self._FRGB)
	
	############# IMG LABEL ###############
	self.imglabel = IMG(self)
	self.imglabel.click.connect(self.clickslot)
	self.imglabel.move.connect(self.moveslot)

	self.imgscroll = QtGui.QScrollArea()
	self.imgscroll.setFixedSize(500, 500)
	self.imgscroll.setWidgetResizable(True)
	self.imgscroll.setWidget(self.imglabel)

	############ Pixel Label ###############
	self.pix = QtGui.QLabel("Pixel: ")
	self.pix.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
	self.pix.setFixedSize(200, 30)

	############ RGB Label #################
	self.rgb = QtGui.QLabel("RGB: ")
	self.rgb.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Raised)
	self.rgb.setFixedSize(300, 30)

	########### Create Windows #############
	self.vlayout.addWidget(self.rgb_rate)
	self.vlayout.addWidget(self.wrgb)
	self.setCentralWidget(self.widget)

	self.h2layout.addWidget(self.pix)
	self.h2layout.addWidget(self.rgb)

	self.v2layout.addWidget(self.imgscroll)
	self.v2layout.addLayout(self.h2layout)

	self.hlayout.addLayout(self.vlayout)
	self.hlayout.addLayout(self.v2layout)
	#self.hlayout.addWidget(self.imgscroll)
	self.hlayout.setAlignment(QtCore.Qt.AlignHCenter)
	self.widget.setLayout(self.hlayout)
	
	self.setWindowTitle("Bitmap Filter")
	self.resize(1000,500)
	self.show()
    
    def infoimg(self):

	self.R = list()
	self.G = list()
	self.B = list()

	self.pic = Image.open(IMGFILE)
	for x in xrange(self.pic.size[0]):
	    for y in xrange(self.pic.size[1]):
		r,g,b = self.pic.getpixel((x,y))
		self.R.append(r)
		self.G.append(g)
		self.B.append(b)
	
	self.R = np.array(self.R)
	self.G = np.array(self.G)
	self.B = np.array(self.B)


    ########## FILTERS RGB ###########
    def _FRGB(self,value):

	self.FRGB = value
	[self._F1,self._F2, self._F3, self._F4, self._F5, self._F6][value]()

    def _F1(self):
	bm = np.asarray(self.pic.convert('L')).copy()
	bm = (np.square(abs(self.RATE * np.arctan(bm) )) % 256)
	self.img = Image.fromarray(bm)
	self.img = self.img.convert("1")
	self.img.save("out.bmp")
	self.imglabel.setPixmap(QtGui.QPixmap("out.bmp"))

    def _F2(self):
	bm = np.asarray(self.pic.convert('L')).copy()
	bm = ((np.sqrt(np.sqrt(self.RATE) * bm)) % 256)
	self.img = Image.fromarray(bm)
	self.img = self.img.convert("1")
	self.img.save("out.bmp")
	self.imglabel.setPixmap(QtGui.QPixmap("out.bmp"))

    def _F3(self):

	bm = np.asarray(self.pic).copy()
	bm = (self.RATE + bm) % 256
	self.img = Image.fromarray(bm, "RGB").convert('1')
	self.img.save("out.bmp")
	self.imglabel.setPixmap(QtGui.QPixmap("out.bmp"))

    def _F4(self):
	bm = np.asarray(self.pic.convert('L')).copy()
	bm = ((abs(np.sin(np.sqrt(self.RATE))) * bm ) % 256)
	self.img = Image.fromarray(bm)
	self.img = self.img.convert("1")
	self.img.save("out.bmp")
	self.imglabel.setPixmap(QtGui.QPixmap("out.bmp"))

    def _F5(self):
	bm = np.asarray(self.pic.convert('L')).copy()
	bm = ((abs(np.tan(self.RATE)) * bm ) % 256)
	self.img = Image.fromarray(bm)
	self.img = self.img.convert("1")
	self.img.save("out.bmp")
	self.imglabel.setPixmap(QtGui.QPixmap("out.bmp"))
    
    def _F6(self):
	bm = np.asarray(self.pic.convert('L')).copy()
	bm[bm <  self.RATE] = 0
	bm[bm >= self.RATE] = 255
	self.img = Image.fromarray(bm)
	self.img = self.img.convert("1")
	self.img.save("out.bmp")
	self.imglabel.setPixmap(QtGui.QPixmap("out.bmp"))
    """
    def _F6(self):
	bm = np.asarray(self.pic.convert('L')).copy()
	bm[bm <  self.RATE] = 0
	bm[bm >= self.RATE] = 255
	self.img = Image.fromarray(bm)
	self.img = self.img.convert("1")
	self.img.save("out.bmp")
	self.imglabel.setPixmap(QtGui.QPixmap.loadFromData(self.img))
    """

    ########## FILTERS RATE ###########
    def _RATE(self,value):

	self.RATE = value
	self._FRGB(self.FRGB)		
	
    ########## SLOTS ##################
    def clickslot(self,args):
	print args

    def moveslot(self,args):
	self.pix.setText(str("Pixel: %s" %args))
	self.rgb.setText(str("RGB: %s" %self.img.getpixel(tuple(args))))

if len(sys.argv) != 2:
    print "Usage: python %s <img.png>" %(sys.argv[0]) 
    sys.exit(1)

IMGFILE =  sys.argv[1]
app 	=  QtGui.QApplication(sys.argv)
ex 	=  Win()
sys.exit(app.exec_())

