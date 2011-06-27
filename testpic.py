#!/usr/bin/python
from mat import *
from math import log
from random import random
step={('y','z','a','b','g'):100,('y','z'):100,('a','b','g'):0.1}
stepx={'x':10**4,'y':10000.0,'z':10000.0,('y','z'):50.0}
stepa={'a':0.1,'b':0.1,'g':0.1,('a','b','g'):0.1}

def readfile(filename):
  f=open(filename,"r")
  p1,p2=[],[]
  l=[] 
  for (i,line) in enumerate(f):
    if i==0:
      f=float(line)
    else:
      (x,y)=map(float,line.split())
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
  F=prunedag(prune(reduce(add,d)),{})
  dl=map(lambda x: prunedag(prune(dt(F,x)),{}),['x','y','z','a','b','g'])
#  dl=map(lambda x: dt(F,x),['x','y','z','a','b','g'])
  return (F,dl)

def optm(F,d,var,v,vf,q=None):
  if q==None: q=[1.0]*len(d)
  vd=map(lambda x:parsedag(x,{},var),d)
  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  tv=[var[x] for x in v]
  while True: 
    for (x,y) in izip(v,p):
      var[x]-=y*step[v]
    tvf=parsedag(F,{},var)
    if tvf>vf:
      for (x,y) in izip(v,tv):
        var[x]=y 
      step[v]/=1.5
    else:
      step[v]*=2.0
      return tvf

def minimize(F,dl):
  var={'x':10000.0,'y':-5912.5,'z':17051.1,'a':0.7,'b':-0.9,'g':0.3} #864
  i=0
  print "iaai"
  vf=parsedag(F,{},var)
  while True:
#    optx(F,dl[0],var,'x')
#    vf=optx(F,dl[1],var,'y',vf)
#    vf=optx(F,dl[2],var,'z',vf)
#    vf=opta(F,dl[3],var,'a',vf)
#    vf=opta(F,dl[4],var,'b',vf)
#    vf=opta(F,dl[5],var,'g',vf)

#    vf=optm(F,(dl[1],dl[2]),var,('y','z'),vf)
#    vf=opt2(F,(dl[1],dl[2]),var,('y','z'),vf)
#    vf=optabg(F,(dl[3],dl[4],dl[5]),var,('a','b','g'),vf)i
    vf=optm(F,(dl[1],dl[2]),var,('y','z'),vf,[1.0,1.0])
    vf=optm(F,(dl[3],dl[4],dl[5]),var,('a','b','g'),vf,[1.0,1.0,1.0])
    print("%f %f %e %e %e %f %d"%(var['y'],var['z'],var['a'],var['b'],var['g'],(vf/6.0)**0.5,i))
#    print("%e ( %.1f %.1f %.1f ) %.1f %.1f %.1f %.0f ( %.2e %.2e %.2e )%d"%
#          ((vf/6.0)**(0.5),var['x'],var['y'],var['z'],var['a'],var['b'],var['g'],stepx[('y','z')],stepa['a'],stepa['b'],stepa['g'],i))
#            parse(dl[0],var),parse(dl[1],var),parse(dl[2],var),parse(dl[3],var),parse(dl[4],var),parse(dl[5],var),i))
# %.2e %.2e %.2e %.2e %.2e %.2e 
    i+=1 

if __name__=="__main__":
  (p1,p2,s,f)=readfile("points2.in")
  vecpic(p1,s,f)  
  (v1,v2)=map(lambda x:vecpic(x,s,f),[p1,p2])
  (F,dl)=system(v1,v2)
#  print(nops(F)) #82307
#  print(prune(dl[0])) #64391
#  print(nops(prune(dl[5])))) #132731
  minimize(F,dl)



     
