#!/usr/bin/python
from mat import *
from math import log
from random import random
step={('y','z','a','b','g'):100,('y','z'):100}
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
#  dl=[]
  dl=map(lambda x: prunedag(prune(dt(F,x)),{}),['x','y','z','a','b','g'])
#  dl=map(lambda x: dt(F,x),['x','y','z','a','b','g'])
  return (F,dl)

def optx(F,d,var,v,vf):
  vd=parsedag(d,{},var)
  tv=var[v]
  if vd>0:
    var[v]-=stepx[v]
  else:
    var[v]+=stepx[v]
  tvf=parsedag(F,{},var)
  if tvf>vf:
    var[v]=tv
    stepx[v]/=1.2
    return vf
  stepx[v]*=1.05
  return tvf

def opt2(F,d,var,v,vf):
  vd1=parsedag(d[0],{},var)
  vd2=parsedag(d[1],{},var)  
  p1=vd1/((vd1**2+vd2**2)**(0.5))
  p2=vd2/((vd1**2+vd2**2)**(0.5))
  tv=(var[v[0]],var[v[1]])
  var[v[0]]-=p1*stepx[v]
  var[v[1]]-=p2*stepx[v]
  tvf=parsedag(F,{},var)
  if tvf>vf:
    var[v[0]],var[v[1]]=tv
    stepx[v]/=1.2
    return vf
  stepx[v]*=1.05
  return tvf

def optabg(F,d,var,v,vf):
  vd1=parsedag(d[0],{},var) 
  vd2=parsedag(d[1],{},var) 
  vd3=parsedag(d[2],{},var)
  sqrt=(vd1**2+vd2**2+vd3**2)**0.5 
  p1=vd1/sqrt
  p2=vd2/sqrt
  p3=vd3/sqrt
  tv=(var[v[0]],var[v[1]],var[v[2]])
  var[v[0]]-=p1*stepa[v]
  var[v[1]]-=p2*stepa[v]
  var[v[2]]-=p3*stepa[v]
  tvf=parsedag(F,{},var)
  if tvf>vf:
    var[v[0]],var[v[1]],var[v[2]]=tv
    stepa[v]/=1.2
    return vf
  stepa[v]*=1.05
  return tvf

def optm(F,d,var,v,vf,q):
  vd=map(lambda x:parsedag(x,{},var),d)
  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  tv=[var[x] for x in v]

  for (x,y) in izip(v,p):
    var[x]-=y*step[v]
  tvf=parsedag(F,{},var)
  if tvf>vf:
    for (x,y) in izip(v,tv):
      var[x]=y 
    step[v]/=1.2
    return vf
  step[v]*=1.05
  return tvf

def opta(F,d,var,v,vf):
  vd=parsedag(d,{},var)
  tv=var[v]
  if vd>0:
    var[v]-=stepa[v]
  else:
    var[v]+=stepa[v]
  tvf=parsedag(F,{},var)
  if tvf>vf:
    var[v]=tv
    stepa[v]/=2.0
    return vf
  stepa[v]*=1.5
  return tvf
 
def minimize(F,dl):
#  var={'x':10000.0,'y':4035.0,'z':-13050.1,'a':6.4,'b':-3.1,'g':-0.3} #9.141
#  var={'x':10000.0,'y':-286.3,'z':5048.3,'a':4.7,'b':-3.2,'g':-1.6} #
#  var={'x':10000.0,'y':1961.8,'z':-9239,'a':-0.2,'b':0.9,'g':0.4} #967.5
#  var={'x':10000.0,'y':5912.5,'z':-17051.1,'a':-0.7,'b':0.9,'g':0.3} #864
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

    vf=optm(F,(dl[1],dl[2],dl[3],dl[4],dl[5]),var,('y','z','a','b','g'),vf,[1.0,1.0,1.0,0.001,0.001,0.001])
    print("%f %f %f %e %e %e %d"%(var['y'],var['z'],var['a'],var['b'],var['g'],(vf/6.0)**0.5,i))
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
  dic={}
  for e in ['a','b','g','x','y','z']:
    dic[e]=random()*10
  dl2=map(lambda x: prunedag(prune(dtold(F,x)),{}),['x','y','z','a','b','g'])
  for (x,y) in izip(dl,dl2):
    v1=parsedag(x,{},dic)  
    v2=parsedag(y,{},dic)
    print "%f %f %d"%(v1,v2,v1==v2) 
   
