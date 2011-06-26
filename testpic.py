#!/usr/bin/python
from mat import *
from math import log
from random import random
stepx={'x':10**4,'y':10**4,'z':10**4}
stepa={'a':1.0,'b':1.0,'g':1.0}
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
  stepx[v]*=1.25
  return tvf
     
def opta(F,d,var,v,vf):
  vd=parse(d,var)
  tv=var[v]
  if vd>0:
    var[v]-=stepa[v]
  else:
    var[v]+=stepa[v]
  tvf=parse(F,var)
  if tvf>vf:
    var[v]=tv
    stepa[v]/=2.0
    return vf
  stepa[v]*=1.25
  return tvf
 
def minimize(F,dl):
#  var={'x':10000.0,'y':4035.0,'z':-13050.1,'a':6.4,'b':-3.1,'g':-0.3} #9.141
  var={'x':10000.0,'y':4035.0,'z':-13050.1,'a':6.4,'b':-3.1,'g':-0.3} #9.141
  i=0 
  while True:
#    optx(F,dl[0],var,'x')
    vf=parse(F,var)
    vf=optx(F,dl[1],var,'y',vf)
    vf=optx(F,dl[2],var,'z',vf)
    vf=opta(F,dl[3],var,'a',vf)
    vf=opta(F,dl[4],var,'b',vf)
    vf=opta(F,dl[5],var,'g',vf)
    var['y']+=-log(random()**0.1)*10
    var['z']+=-log(random()**0.1)*10
    var['a']+=-log(random()**0.1)/10
    var['b']+=-log(random()**0.1)/10
    var['g']+=-log(random()**0.1)/10
    print("%e ( %.1f %.1f %.1f ) %.1f %.1f %.1f %.0f %.0f %.0f ( %.2f %.2f %.2f )%d"%
          ((vf/6.0)**(0.5),var['x'],var['y'],var['z'],var['a'],var['b'],var['g'],stepx['x'],stepx['y'],stepx['z'],stepa['a'],stepa['b'],stepa['g'],i))
#            parse(dl[0],var),parse(dl[1],var),parse(dl[2],var),parse(dl[3],var),parse(dl[4],var),parse(dl[5],var),i))
# %.2e %.2e %.2e %.2e %.2e %.2e 
    i+=1 

if __name__=="__main__":
  (p1,p2,s,f)=readfile("points2.in")
  vecpic(p1,s,f)  
  (v1,v2)=map(lambda x:vecpic(x,s,f),[p1,p2])
  (F,dl)=system(v1,v2) 
  minimize(F,dl)



     
