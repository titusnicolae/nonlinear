#!/usr/bin/python
import sys
import math
from itertools import izip
from copy import copy
from numpy import *

class Xpm:
	def __init__(self,width,height):
		self.width=width;
		self.height=height
		self.colorTable=[]
		self.data=zeros((height,width))
		self.rectangle(Point(0,0),Point(width,height),"white")

	def colorIndex(self,color):
		if isinstance(color,basestring):
			color=self.translateColor(color)
		if color not in self.colorTable:
			self.colorTable.append(color)
		return self.colorTable.index(color)

	def rectangle(self, p1, p2, color):
		colorIndex=self.colorIndex(color) 		
		X=p1.x,p2.x
		Y=p1.y,p2.y
		for x in range(min(X),max(X)):
			for y in range(min(Y),max(Y)):
				self.data[x,y]=colorIndex

	def putPixel(self,x,y,color):
		self.data[x,y]=self.colorIndex(color)
		
	def translateColor(self,colorName):
		if   colorName == "red"  : return Color(255,0,0)
		elif colorName == "green": return Color(0,255,0)
		elif colorName == "blue" : return Color(0,0,255)
		elif colorName == "white": return Color(255,255,255)
		else:                      return Color(0,0,0)

	def write(self,path):
		f=open(path,"w")
		f.write("/* XPM */\n")
		f.write("static char *egc[] = {\n\n")
		f.write("/* width,height,nrcolors,charsperpixel */\n")
		f.write("\" %d %d %d %d \",\n\n" % (self.width,self.height,len(self.colorTable),1))
		f.write("/* colors #RRGGBB */\n")

		for i,color in enumerate(self.colorTable):
			f.write("\"%c c #%02X%02X%02X\",\n" % (i+97,color.red,color.green,color.blue))
		f.write("\n\n/* pixels */\n");
		for y in range(self.height):
			f.write("\"")
			for x in range(self.width):
				f.write("%c" % int(self.data[x,self.height-1-y]+97))
			if x!=self.height-1:
				f.write("\",\n")
			else:
				f.write("\"\n")
		f.write("};")
		f.close()
	def drawWindow(self,w,color):
		self.drawLine(w.x1,w.y1,w.x1,w.y2,color)
		self.drawLine(w.x1,w.y2,w.x2,w.y2,color)
		self.drawLine(w.x2,w.y2,w.x2,w.y1,color)
		self.drawLine(w.x2,w.y1,w.x1,w.y1,color)

	def drawLine(self,param1,param2,param3=None,param4=None,param5=None):
		if param4==None:
			p1=Point(int(param1.x),int(param1.y))
			p2=Point(int(param2.x),int(param2.y))
			if param3 is None:
				color="black"
			else:
				color=param3
		else:
			p1=Point(int(param1),int(param2))
			p2=Point(int(param3),int(param4))
			if param5!=None:
				color=param5	
			else:
				color="black"
	
		a,b,c=p1.y-p2.y,p2.x-p1.x,p2.x*p1.y-p2.y*p1.x
		romb=(abs(a)<abs(b))
		patrat=sgn((p2.y-p1.y)*(p2.x-p1.x))
		dirx=1 if p2.x>p1.x else -1
		diry=1 if p2.y>p1.y else -1		
		if p1.x==p2.x and p1.y==p2.y:
			self.putPixel(p1.x,p1.y,color)
			return
		x,y=0,0
		if(romb):
			while abs(x)<=abs(p2.x-p1.x):
				if patrat*(2*a*x+2*b*y+b*diry)<0:
					y+=diry
				self.putPixel(p1.x+x,p1.y+y,color)
				x+=sgn(p2.x-p1.x)
		else:
			while abs(y)<=abs(p2.y-p1.y):
				if patrat*(2*a*x+2*b*y+a*dirx)>0:	
					x+=dirx
				self.putPixel(p1.x+x,p1.y+y,color)				
				y+=sgn(p2.y-p1.y)

	def drawBezier(self, pl, prec):
		l=[]
		temp=dot(array([[-1,3,-3,1],[3,-6,3,0],[-3,3,0,0],[1,0,0,0]]),array(pl))
		for i in range(0,int(1.0/prec)):
			t=i*prec
			l.append(dot(array([t**3,t**2,t,1]),temp))
		l.append(dot(array([1,1,1,1]),temp))
		for a,b in izip(l[:-1],l[1:]):
			self.drawLine(a,b)


	def bit(self ,p, w):
		mask=0
		if p.x<w.x1:	mask|=0x01
		elif p.x>w.x2: mask|=0x02
		if p.y<w.y1:    mask|=0x10
		elif p.y>w.y2: mask|=0x20
		return mask
	
	def fit(self,p1,p2,w):
		p=Point(p1.x,p1.y)
		m=self.bit(p,w)
		if p1.y!=p2.y and m&0x30:
			p.y=w.y1 if m&0x10 else w.y2-1
			p.x=int((p.y-p2.y)*(p1.x-p2.x)/(p1.y-p2.y)+p2.x)
		m=self.bit(p,w)
		if (m&0x03) and p1.x-p2.x>0:
			p.x=w.x1 if m&0x01 else w.x2-1
			p.y=int((p.x-p2.x)*(p1.y-p2.y)/(p1.x-p2.x)+p2.y)
		return p

	def drawClippedLine(self,w,p1,p2,color):
		m1,m2=self.bit(p1,w),self.bit(p2,w)
		if m1&m2: return 
		if m1==0 and m2==0:
			self.drawLine(p1,p2,color)
			return
		p1,p2=self.fit(p1,p2,w),self.fit(p2,p1,w)
		if self.bit(p1,w)==0 and self.bit(p2,w)==0:
			self.drawLine(p1,p2,color)
			return
	
def abs(x):
	if x<0: return -x
	else: return x

def sgn(x):
	if x==0: return 0
	elif x<0: return -1
	else: return 1


class Window:
	def __init__(self,p1,p2=None,p3=None,p4=None):
		if p2==None and p3==None and p4==None:
			self.x1,self.y1,self.x2,self.y2=p1
		elif p3==None and p4==None:
			self.x1,self.y1=p1.x,p1.y
			self.x2,self.y2=p2.x,p2.y
		else:
			self.x1,self.y1,self.x2,self.y2=p1,p2,p3,p4
	def __repr__(self):
		return "("+str(self.x1)+","+str(self.y1)+"|"+str(self.x2)+","+str(self.y2)+")"

class Color:
	def __init__(self,red,green,blue):
		self.red=red
		self.blue=blue
		self.green=green

	def __eq__(self,other):
		if self.red==other.red and self.blue==other.blue and self.green==other.green:
			return True
		return False
	
	def __repr__(self):
		return "(r="+str(self.red)+",g="+str(self.green)+",b="+str(self.blue)+")"

class Point:
	def __init__(self,p,q=None):
		if q!=None:
			self.x,self.y=p,q
		elif isinstance(p,Point):
			self.x,self.y=p.x,p.y
		else:
			self.x,self.y=p

	def __repr__(self):
		return "("+str(self.x)+","+str(self.y)+")"
	def __eq__(self,other):
		if math.sqrt((self.x-other.x)**2+(self.y-other.y)**2)<=5:
			return True
		return False 
	def __mul__(self,factor):
		return Point(self.x*factor,self.y*factor)
	def __rmul__(self,factor):
		return Point(self.x*factor,self.y*factor)
	def __add__(self,other):
		return Point(self.x+other.x,self.y+other.y)
 
	def array(self):
		return array([self.x,self.y,1])

def processParameters(l):
        if len(sys.argv)!=2*len(l)+1:
                print "Insuficient number of parameters"
                return
        for p in sys.argv[1::2]:
                if p not in l:
                        print "Incorect parameter"
                        return
        d={}

        for p,q in izip(sys.argv[1::2],sys.argv[2::2]):
                d[p]=q
        return d

if __name__ == "__main__":
	x=Xpm(100,100)
	x.drawLine(Point(30,0),Point(20,20),"black")	
	x.write("caca.xpm")

