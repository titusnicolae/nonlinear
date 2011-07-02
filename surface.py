#!/usr/bin/python
from xpm import *
from itertools import izip
import sys
xpm=Xpm(1000,1000)
f=open("file.o","r")

for line in f:
  if len(line.split())>4 and i>2:
    l.append(map(float,[line.split()[0],line.split()[1]])) 
  i+=1
st=5
s=l[st]
color="black"
ox=0.0
oy=900.0
if len(sys.argv)==3:
  sx=sy=float(sys.argv[2])
elif len(sys.argv)==4:
  sx=float(sys.argv[2])
  sy=float(sys.argv[3])
else:
  sx=sy=10.0    
for e,f in izip(l[st:-1],l[st+1:]):
  xpm.drawLine(Point(ox+(e[0]-s[0])/sx,oy+(e[1]-s[1])/sy),Point(ox+(f[0]-s[0])/sx,oy+(f[1]-s[1])/sy),Colorcolor)
  if color=="black":
    color="red"
  elif color=="red":
    color="black" 
xpm.write(sys.argv[1]+".xpm")



