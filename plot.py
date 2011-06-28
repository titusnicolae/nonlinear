#!/usr/bin/python
from xpm import *
from itertools import izip
xpm=Xpm(1000,1000)
f=open("file.o","r")
l=[]
i=0

for line in f:
  if len(line.split())==9:
    l.append(map(float,[line.split()[0],line.split()[5]])) 
  i+=1
st=20
s=l[st]
color="black"
ox=500.0
oy=500.0
sx=10.0
sy=0.001
for e,f in izip(l[st+1:-1],l[st+2:]):
  xpm.drawLine(Point(ox+(e[0]-s[0])/sx,oy+(e[1]-s[1])/sy),Point(ox+(f[0]-s[0])/sx,oy+(f[1]-s[1])/sy),color)
  if color=="black":
    color="red"
  elif color=="red":
    color="black" 

xpm.write('out.xpm')   



