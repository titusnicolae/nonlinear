#!/usr/bin/python2.6
from matx import *
from math import log
from random import random
from time import clock
import psyco
psyco.bind(parsedag)
psyco.bind(curry)
tstart=clock()

step2={('y','z'):100.0}
step={('y','z','a','b','g'):100,('y','z'):100,('a','b','g'):0.01,('a',):0.1,('b',):0.1,('g',):0.1,'a':0.1,'b':0.1,'g':0.1}
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
    return (F,dl,d)
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

def crazymx(F,d,var,v,vf,q=None,cu=None,stepup=None):
  dbg=False
  if q==None: q=[1.0]*len(d)
  if cu!=None: Fcu=curry(F,cu)
  else: Fcu=F
  vd=map(lambda x:parsedag(x,{},var),d)
  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  tvv=[var[x] for x in v]
  for (x,y) in izip(v,p):
    var[x]-=y*step[v] 
   
  vd=map(lambda x:parsedag(x,{},var),d)
  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  tv=[var[x] for x in v]
  i=0
  step2[('y','z')]=step[('y','z')]*4
  while True and i<100: 
    i+=1
    for (x,y) in izip(v,p):
      var[x]-=y*step2[v]
    tvf=parsedag(Fcu,{},var)
    if tvf>vf:
      for (x,y) in izip(v,tv):
        var[x]=y 
      step2[v]/=1.2
    else:
      step2[v]*=2.0
      return tvf
  for (x,y) in izip(v,tvv):
    var[x]=y
  if dbg and gdbg: print "damn"
  return vf

#def printPartial(tree,depth=None): #
#  if depth==None:
#    return printPartial(tree,0)  
#  else:
#    print tree

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

def optmx2(F,d,var,v,vf,q=None,cu=None,stepup=None):
  if q==None: q=[1.0]*len(d)
  if cu!=None: Fcu=curry(F,cu)
  else: Fcu=F
  vd=map(lambda x:parsedag(x,{},var),d)
  try:
    sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  except:
    print vd,q
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  tv=[var[x] for x in v]
  stop=False 
  while True: 
    for (x,y) in izip(v,p):
      var[x]-=y*step[v]
    tvf=parsedag(Fcu,{},var)
    if tvf>vf:
      for (x,y) in izip(v,tv):
        var[x]=y 
      step[v]/=1.1
      stop=True
    else:
      if stop:
        step[v]*=stepup
        return (vd[0],tvf)
      else:
        for (x,y) in izip(v,tv):
          var[x]=y
        step[v]*=1.1        
       
def optmxbin(F,d,var,v,vf,q=None,cu=None,stepup=None):
  if q==None: q=[1.0]*len(d)
  if cu!=None: Fcu=curry(F,cu)
  else: Fcu=F
  vd=map(lambda x:parsedag(x,{},var),d)
  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  td={}
  dbg=False
  for e in var: td[e]=var[e]
  st=0.0
  dr=step[v]*10.0
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

def optmxbinall(F,d,var,v,vf,q=None,cu=None,stepup=None):
  if q==None: q=[1.0]*len(d)
  if cu!=None: Fcu=curry(F,cu)
  else: Fcu=F
  vd=map(lambda x:parsedag(x,{},var),d)
  sqrtx=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd[:2],q[:2]))))**0.5
  px=map(lambda (x,y):x*y/sqrtx,izip(vd[:2],q[:2]))  
  sqrta=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd[2:],q[2:]))))**0.5
  pa=map(lambda (x,y):x*y/sqrta,izip(vd[2:],q[2:]))

  td={}
  dbg=False
  stx=sta=0.0
  vx=('y','z')
  va=('a','b','g')
  drx=step[vx]*2.0
  dra=step[va]*2.0

  td=var.copy()
  for (x,y) in izip(va,pa): td[x]=var[x]-y*(dra-sta)/2.0
  for (x,y) in izip(vx,px): td[x]=var[x]-y*stx
  vstx=parsedag(Fcu,{},td)

  td=var.copy()
  for (x,y) in izip(va,pa): td[x]=var[x]-y*(dra-sta)/2.0
  for (x,y) in izip(vx,px): td[x]=var[x]-y*drx
  vdrx=parsedag(Fcu,{},td)

  td=var.copy()
  for (x,y) in izip(va,pa): td[x]=var[x]-y*sta
  for (x,y) in izip(vx,px): td[x]=var[x]-y*(drx-stx)/2.0
  vsta=parsedag(Fcu,{},td)

  td=var.copy()
  for (x,y) in izip(va,pa): td[x]=var[x]-y*dra
  for (x,y) in izip(vx,px): td[x]=var[x]-y*(drx-stx)/2.0
  vdra=parsedag(Fcu,{},td)

  difx=(drx-stx)/10.0**5
  difa=(dra-sta)/10.0**5
  vmi=0

  while stx+difx<drx and sta+difa<dra:
    mix=(stx+drx)/2.0
    mia=(sta+dra)/2.0

    td=var.copy()
    for (x,y) in izip(vx,px): td[x]=var[x]-y*mix
    for (x,y) in izip(va,pa): td[x]=var[x]-y*mia
    vmi=parsedag(Fcu,{},td)
  
    if dbg: print "[%e %e] (%e %e) [%e %e] (%e %e) {%e}"%(stx,drx,sta,dra,vstx,vdrx,vsta,vdra,vmi)
 
    if vmi > vstx and vmi > vdrx:
      if vstx<vdrx:
        if dbg: print "1"
        drx=mix
      else:
        if dbg: print "2"
        stx=mix
    elif vmi<vstx and vmi<vdrx:
      if vstx<vdrx:
        if dbg: print "3"
        drx=mix
      else:
        if dbg: print "4"
        stx=mix
    elif vmi<vstx or vmi<vdrx:
      if vstx<vdrx:
        if dbg: print "5"
        drx=mix
      else:
        if dbg: print "6"
        stx=mix

    if vmi > vsta and vmi > vdra:
      if vsta<vdra:
        if dbg: print "1"
        dra=mia
      else:
        if dbg: print "2"
        sta=mia
    elif vmi<vsta and vmi<vdra:
      if vsta<vdra:
        if dbg: print "3"
        dra=mia
      else:
        if dbg: print "4"
        sta=mia
    elif vmi<vsta or vmi<vdra:
      if vsta<vdra:
        if dbg: print "5"
        dra=mia
      else:
        if dbg: print "6"
        sta=mia

    td=var.copy()
    for (x,y) in izip(va,pa): td[x]=var[x]-y*(dra-sta)/2.0
    for (x,y) in izip(vx,px): td[x]=var[x]-y*stx
    vstx=parsedag(Fcu,{},td)

    td=var.copy()
    for (x,y) in izip(va,pa): td[x]=var[x]-y*(dra-sta)/2.0
    for (x,y) in izip(vx,px): td[x]=var[x]-y*drx
    vdrx=parsedag(Fcu,{},td)

    td=var.copy()
    for (x,y) in izip(va,pa): td[x]=var[x]-y*sta
    for (x,y) in izip(vx,px): td[x]=var[x]-y*(drx-stx)/2.0
    vsta=parsedag(Fcu,{},td)

    td=var.copy()
    for (x,y) in izip(va,pa): td[x]=var[x]-y*dra
    for (x,y) in izip(vx,px): td[x]=var[x]-y*(drx-stx)/2.0
    vdra=parsedag(Fcu,{},td)

  step[vx]=mix+1
  step[va]=mia+0.01
  for (x,y) in izip(vx,px): var[x]=var[x]-y*mix
  for (x,y) in izip(va,pa): var[x]=var[x]-y*mia
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
  var['y']=random()*20000-10000 
  var['z']=random()*20000-10000 
  var['a']=random()*3.14-1.57
  var['b']=random()*3.14-1.57
  var['g']=random()*3.14-1.57
  return var

def resetstep():
  step[('y','z')]=100.0
  step[('a',)]=0.1
  step[('b',)]=0.1
  step[('g',)]=0.1

def printshit(var,vf,j,mode=None):
	print("%.4f %.4f (%.4f) %.6f %.6f %.6f (%.6e) %f %d mode %d"%(var['y'],var['z'],step[('y','z')],var['a'],var['b'],var['g'],step[('a','b','g')],((vf)**0.5)/6.0,j,mode))

def minimize(F,dl,deltaList):
  mode=1
  #var={'x':10000.0,'y':-1683.3819,'z':3601.4280,'a':-0.0736,'b':-0.5574,'g':-0.2129} 
  var={'x':10000.0,'y':0.0,'z':0.0,'a':0.0,'b':0.0,'g':0.0} 
#864
#  var=randomize()
  print var
  print clock()-tstart
  j=0
  vf=parsedag(F,{},var)
  pvf=1.0
  dbg=True
  dbgmode=False
  dbgtime=False
  deltaEval=[]
  while True:
   # deltaEval=[]
 #   for x in deltaList: 
  #    deltaEval.append(parsedag(x,{},var))
#    print("%06.6f %06.6f %06.6f %06.6f %06.6f %06.6f"%(deltaEval[0],deltaEval[1],deltaEval[2],deltaEval[3],deltaEval[4],deltaEval[5]))  
    if clock()-tstart>6000.0: 
        printshit(var,vf,j,mode)
        break

    if mode==1:
      #vf,pvf=optmxbinall(F,(dl[1],dl[2],dl[3],dl[4],dl[5]),var,('y','z','a','b','g'),vf,stepup=2.0),vf
      vf,pvf=optmxbin(F,(dl[1],dl[2]),var,('y','z'),vf,cu={'a':var['a'],'b':var['b'],'g':var['g'],'x':var['x']},stepup=2.0),vf
      if dbg and gdbg and dbgmode:    
        print "mode 1"
      if dbg and gdbg:
        printshit(var,vf,j,mode)
      if vf/pvf>0.999:
        if gdbg and dbgtime:
          print clock()-tstart 
        mode=2     
    elif mode==2:
      pvf=vf
  
      #vf,pvf=optmxbinall(F,(dl[1],dl[2],dl[3],dl[4],dl[5]),var,('y','z','a','b','g'),vf,stepup=2.0),vf
      vf,pvf=optmxbin(F,(dl[1],dl[2]),var,('y','z'),vf,cu={'a':var['a'],'b':var['b'],'g':var['g'],'x':var['x']},stepup=2.0),vf
      #if j%2==0:
      #  vf=crazymx(F,(dl[1],dl[2]),var,('y','z'),vf,cu={'a':var['a'],'b':var['b'],'g':var['g'],'x':var['x']},stepup=2.0)
      #if j%2==1:
      #  vf=optmx(F,(dl[1],dl[2]),var,('y','z'),vf,cu={'a':var['a'],'b':var['b'],'g':var['g'],'x':var['x']},stepup=2.0)
      if j%3==0:
        cu=var.copy()
        del cu['a']
        (pda,vf)=optmx2(F,(dl[3],),var,('a',),vf,stepup=1.0)
      elif j%3==1:
        cu=var.copy()
        del cu['b']
        (pdb,vf)=optmx2(F,(dl[4],),var,('b',),vf,stepup=1.0)
      elif j%3==2:
        cu=var.copy()
        del cu['g']
        (pdg,vf)=optmx2(F,(dl[5],),var,('g',),vf,stepup=1.0)
      
      j+=1
      if dbg and gdbg and dbgmode:    
        print "mode 2"
      if j%2 and dbg and gdbg:
        printshit(var,vf,j,mode)
#      if vf/pvf>0.9995:
#        mode=3 

    elif mode==3:
      if gdbg and dbgtime:
        print "mode 3 %d"%(clock()-tstart)
      vf,pvf=optmxbinall(F,(dl[1],dl[2],dl[3],dl[4],dl[5]),var,('y','z','a','b','g'),vf,stepup=2.0),vf
      if dbg and gdbg:
        printshit(var,vf,j,mode)
         

if __name__=="__main__":
  (p1,p2,s,f)=readfile("livingroomx.in")
  vecpic(p1,s,f)  
  (v1,v2)=map(lambda x:vecpic(x,s,f),[p1,p2])
  (F,dl,deltaList)=system(v1,v2) 
  minimize(F,dl,deltaList)
