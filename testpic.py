#!/usr/bin/python
from mat import *
stepx={'x':1000.0,'y':1000.0,'z':1000.0}
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
 
def system(v1,v2):
  d=[]
  s=['x','y','z']
  r=['a','b','g']
  for (p1,p2) in izip(v1,v2):
    d.append(delta(p1,p2,s,r))
  F=reduce(add,d)
  dl=map(lambda x: prune(dt(F,x)),['x','y','z','a','b','g'])
# dl=map(lambda x: dt(F,x),['x','y','z','a','b','g'])
  return (F,dl)

def optx(F,d,var,v,vf):
  vd=parse(d,var)
  tv=var[v]
  if vd>0:
    var[v]-=stepx[v]
  else:
    var[v]+=stepx[v]
  tvf=parse(F,var)
  if tvf>vf:
    var[v]=tv
    stepx[v]/=2.0
    return vf
  return tvf
     
def opta(F,d,var,v):
  vd=parse(d,var)
  if vd>0:
    var[v]-=0.01
  else:
    var[v]+=0.01
 
def minimize(F,dl):
  var={'x':-10000,'y':7000,'z':1000,'a':2.9,'b':-0.3,'g':-0.5}
  i=0 
  while True:
#    optx(F,dl[0],var,'x')
    vf=parse(F,var)
    vf=optx(F,dl[1],var,'y',vf)
    vf=optx(F,dl[2],var,'z',vf)
    opta(F,dl[3],var,'a')
    opta(F,dl[4],var,'b')
    opta(F,dl[5],var,'g')
    print("%.1f %.1f %.1f %.1f %.2f %.2f %.2f %1.f %1.f %1.f %d"%(parse(F,var),var['x'],var['y'],var['z'],var['a'],var['b'],var['g'],stepx['x'],stepx['y'],stepx['z'],i))
    i+=1 

if __name__=="__main__":
  (p1,p2,s,f)=readfile("points.in")
  vecpic(p1,s,f)  
  (v1,v2)=map(lambda x:vecpic(x,s,f),[p1,p2])
  (F,dl)=system(v1,v2) 
  minimize(F,dl)



     
