#!/usr/bin/python
from mat import *

def readfile(filename):
  f=open(filename,"r")
  p1,p2=[],[]
  l=[] 
  for (i,line) in enumerate(f):
    if i==0:
      f=float(line)
    else:
      (x,y)=map(int,line.split())
      l.append((x,y))
  s=l[0]
  p1=l[1:7]
  p2=l[7:]
  return (p1,p2,s,f)

def vecpic(l,s,f):
  c=map(lambda x:x/2, s) 
  r=[]
  for (x,y) in l:
    r.append([x-c[0],y-c[1],f])
  return r
 
def (v1,v2):
  d=[]
  s=['x','y','z']
  r=['a','b','g']
  for (p1,p2) in izip(v1,v2):
    d.append(delta(p1,p2,s,r))
  F=reduce(add,d)
  dl=map(lambda x: prune(dt(F,x)),['x','y','z','a','b','g'])
 
if __name__=="__main__":
  (p1,p2,s,f)=readfile("points.in")
  vecpic(p1,s,f)  
  (v1,v2)=map(lambda x:vecpic(x,s,f),[p1,p2])
  doshit(v1,v2) 
