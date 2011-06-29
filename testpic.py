#!/usr/bin/python
from mat import *
from math import log
from random import random
step={('y','z','a','b','g'):100,('y','z'):100,('a','b','g'):0.1,('a',):0.1,('b',):0.1,('g',):0.1}
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

def optm(F,d,var,v,vf,q=None,cu=None,stepup=None):
  if q==None: q=[1.0]*len(d)
  if cu!=None: Fcu=curry(F,cu)
  else: Fcu=F
  vd=map(lambda x:parsedag(x,{},var),d)
  print "%s %e"%(v,vd[0])
  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  tv=[var[x] for x in v]
  while True: 
    for (x,y) in izip(v,p):
      var[x]-=y*step[v]
    tvf=parsedag(Fcu,{},var)
    if tvf>vf:
      for (x,y) in izip(v,tv):
        var[x]=y 
      step[v]/=1.5
    else:
      step[v]*=stepup
      return tvf

def optmx(F,d,var,v,vf,q=None,cu=None,stepup=None):
  if q==None: q=[1.0]*len(d)
  if cu!=None: Fcu=curry(F,cu)
  else: Fcu=F
  vd=map(lambda x:parsedag(x,{},var),d)
  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  tv=[var[x] for x in v]
  while True: 
    for (x,y) in izip(v,p):
      var[x]-=y*step[v]
    tvf=parsedag(Fcu,{},var)
    if tvf>vf:
      for (x,y) in izip(v,tv):
        var[x]=y 
      step[v]/=1.1
    else:
      step[v]*=stepup
      return tvf

def optmxbin(F,d,var,v,vf,q=None,cu=None,stepup=None):
  if q==None: q=[1.0]*len(d)
  if cu!=None: Fcu=curry(F,cu)
  else: Fcu=F
  vd=map(lambda x:parsedag(x,{},var),d)
  print "%s %e"%(v,vd[0])
  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  td={}
  for e in var: td[e]=var[e]
  st=0.0
  dr=step[v]*16.0
  for (x,y) in izip(v,p): td[x]=var[x]-y*st
  vst=parsedag(Fcu,{},td)
  for (x,y) in izip(v,p): td[x]=var[x]-y*dr
  vdr=parsedag(Fcu,{},td)
  dif=(dr-st)/10.0**5
  while st+dif<dr: 
    mi=(st+dr)/2.0
    for (x,y) in izip(v,p): td[x]=var[x]-y*mi
    vmi=parsedag(Fcu,{},td)
    if vmi > vst and vmi > vdr:
      if vst<vdr:
        dr,vdr=mi,vmi
      else:
        st,vst=mi,vmi
    elif vmi<vst and vmi<vdr:
      if vst<vdr:
        dr,vdr=mi,vmi
      else:
        st,vst=mi,vmi
    elif vmi<vst or vmi<vdr:
      if vst<vdr:
        dr,vdr=mi,vmi  
      else:
        st,vst=mi,vmi
  step[v]=mi+1
  for (x,y) in izip(v,p): var[x]=var[x]-y*mi
  return vmi

def minimize(F,dl):
#  var={'x':10000.0,'y':-5912.5,'z':17051.1,'a':0.7,'b':-0.9,'g':0.3} #864
  var={'x':10000.0,'y':random()*20000.0-10000.0,'z':random()*20000-10000,'a':random()*2-1,'b':random()*2-1,'g':random()*2-1} #864
  i=0
  j=0
  vf=parsedag(F,{},var)
  while True:
    vf=optmxbin(F,(dl[1],dl[2]),var,('y','z'),vf,cu={'a':var['a'],'b':var['b'],'g':var['g']},stepup=2.0)
    if j%3==0:
      vf=optm(F,(dl[3],),var,('a',),vf,stepup=2.0)
    elif j%3==1:
      vf=optm(F,(dl[4],),var,('b',),vf,stepup=2.0)
    elif j%3==2:
      vf=optm(F,(dl[5],),var,('g',),vf,stepup=2.0)
    j+=1
    print("%.1f %.1f (%.1f) %.2f %.2f %.2f (%.2f) %f %d"%(var['y'],var['z'],step[('y','z')],var['a'],var['b'],var['g'],step[('a','b','g')],(vf/6.0)**0.5,i))
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



     
