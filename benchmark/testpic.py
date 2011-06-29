#!/usr/bin/python
from mat import *
from math import log
from random import random

step={('y','z','a','b','g'):100,('y','z'):100,('a','b','g'):0.1,('a',):0.1,('b',):0.1,('g',):0.1,'a':0.1,'b':0.1,'g':0.1}
stepx={'x':10**4,'y':10000.0,'z':10000.0,('y','z'):50.0}
stepa={'a':0.1,'b':0.1,'g':0.1,('a','b','g'):0.1}
gdbg=True
logfile="log.o"
output="out.o"

flog=open(logfile,"w")
fout=open(output,"w")

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
 
def system(v1,v2,d2=None):
  d=[]
  s=['x','y','z']
  r=['a','b','g']
  for (p1,p2) in izip(v1,v2):
    d.append(delta(p1,p2,s,r))
  F=prunedag(prune(reduce(add,d)),{})
  dl=map(lambda x: prunedag(prune(dt(F,x)),{}),s+r)
  if d2==True:
    d2=map(lambda x,y:prunedag(prune(dt(x,y)),{}),dl,s+r) 
    return (F,dl,d2)
  else:
    return (F,dl)
#  dl=map(lambda x: dt(F,x),['x','y','z','a','b','g'])

def optm(F,d,var,v,vf,q=None,cu=None,stepup=None):
  if q==None: q=[1.0]*len(d)
  if cu!=None: Fcu=curry(F,cu)
  else: Fcu=F
  vd=map(lambda x:parsedag(x,{},var),d)
  dbg=False 
  if dbg and gdbg: print "%s %e"%(v,vd[0])
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


def optmd2(F,d,d2,var,v,vf,stepup=None):
  vd =parsedag(d,{},var)
  vd2=parsedag(d2,{},var)
  if vd2>0:
    var[v]-=vd/vd2
    step[v]=vd/vd2
    print "yeah %f" %(vd/vd2)
    return parsedag(F,{},var)
  tv=var[v]
  while True: 
    var[v]-=step[v]
    tvf=parsedag(F,{},var)
    if tvf>vf:
      var[v]=tv 
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
  dbg=False
  for e in var: td[e]=var[e]
  st=0.0
  dr=step[v]*2.0
  for (x,y) in izip(v,p): td[x]=var[x]-y*st
  vst=parsedag(Fcu,{},td)
  for (x,y) in izip(v,p): td[x]=var[x]-y*dr
  vdr=parsedag(Fcu,{},td)
  dif=(dr-st)/10.0**5
  vmi=0
  while st+dif<dr:
    mi=(st+dr)/2.0
    for (x,y) in izip(v,p): td[x]=var[x]-y*mi
    vmi=parsedag(Fcu,{},td)
    if dbg: print "%e %e %e %e %e %e"%(st,mi,dr,vst,vmi,vdr)
    if vmi > vst and vmi > vdr:
      if vst<vdr:
        if dbg: print "1"
        dr,vdr=mi,vmi
      else:
        if dbg: print "2"
        st,vst=mi,vmi
    elif vmi<vst and vmi<vdr:
      if vst<vdr:
        if dbg: print "3"
        dr,vdr=mi,vmi
      else:
        if dbg: print "4"
        st,vst=mi,vmi
    elif vmi<vst or vmi<vdr:
      if vst<vdr:
        if dbg: print "5"
        dr,vdr=mi,vmi  
      else:
        if dbg: print "6"
        st,vst=mi,vmi
  step[v]=mi+1
  for (x,y) in izip(v,p): var[x]=var[x]-y*mi
  return vmi

def optmabin(F,d,var,v,vf,q=None,cu=None,stepup=None):#o singura variabila
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
  dr=step[v]*3.0
  for (x,y) in izip(v,p): td[x]=var[x]-y*st
  vst=parsedag(Fcu,{},td)
  for (x,y) in izip(v,p): td[x]=var[x]-y*dr
  vdr=parsedag(Fcu,{},td)
  dif=(dr-st)/10.0**6
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
def sgn(x):
  if x>=0: return 1
  else: return u

def score(s):
  return (s/6.0)**0.5 
 
def randomize():
  var={}
  var['x']=10000.0
  var['y']=random()*20000-100000 
  var['z']=random()*20000-100000 
  var['a']=random()*3.14-1.57
  var['b']=random()*3.14-1.57
  var['g']=random()*3.14-1.57
  return var

def resetstep():
  step[('y','z')]=100.0
  step[('a',)]=0.1
  step[('b',)]=0.1
  step[('g',)]=0.1

def printshit(var,vf,j):
  print("%.1f %.1f (%.1f) %.2f %.2f %.2f (%.2f) %f %d"%(var['y'],var['z'],step[('y','z')],var['a'],var['b'],var['g'],step[('a','b','g')],(vf/6.0)**0.5,j))

def minimize(F,dl,d2=None):
  mode=1
  var={'x':10000.0,'y':-5912.5,'z':17051.1,'a':0.7,'b':-0.9,'g':0.3} #864
  var=randomize()
  j=0
  vf=parsedag(F,{},var)
  pvf=1.0
  dbg=True 
  while True:
    if mode==1:
      vf,pvf=optmx(F,(dl[1],dl[2]),var,('y','z'),vf,cu={'a':var['a'],'b':var['b'],'g':var['g'],'x':var['x']},stepup=2.0),vf
      if dbg and gdbg:    
        print "mode 1"
        printshit(var,vf,j)
      if vf/pvf>0.999: 
        mode=2      
    else:
      pvf=vf
      vf=optmx(F,(dl[1],dl[2]),var,('y','z'),vf,cu={'a':var['a'],'b':var['b'],'g':var['g'],'x':var['x']},stepup=2.0)
      if j%3==0:
        vf=optm(F,(dl[3],),var,('a',),vf,stepup=2.0)
      elif j%3==1:
        vf=optm(F,(dl[4],),var,('b',),vf,stepup=2.0)
      elif j%3==2:
        vf=optm(F,(dl[5],),var,('g',),vf,stepup=2.0)
      j+=1

      if vf/pvf>0.9999: 
        var=randomize()
        resetstep()
        vf=parsedag(F,{},var)
        j=0
      if dbg and gdbg:    
        print "mode 2"
        printshit(var,vf,j)
      if score(vf)<100: break
  print("%.1f %.1f (%.1f) %.2f %.2f %.2f (%.2f) %f %d"%(var['y'],var['z'],step[('y','z')],var['a'],var['b'],var['g'],step[('a','b','g')],(vf/6.0)**0.5,j))

if __name__=="__main__":
  (p1,p2,s,f)=readfile("points2.in")
  vecpic(p1,s,f)  
  (v1,v2)=map(lambda x:vecpic(x,s,f),[p1,p2])
  (F,dl)=system(v1,v2)
  minimize(F,dl)



     
