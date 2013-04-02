#!/usr/bin/python2.6
from matx import *
from math import log
from random import random
from time import clock
import psyco
import nonlinear
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


def optmx2(F,d,var,v,vf,q=None,cu=None,stepup=None):
  if q==None: q=[1.0]*len(d)
  #if cu!=None: Fcu=curry(F,cu)
  #else: Fcu=F
  
  if   v[0]=='a':
    vd=[nonlinear.d3(var['a'],var['b'],var['g'],var['x'],var['y'],var['z'])]
  elif v[0]=='b':
    vd=[nonlinear.d4(var['a'],var['b'],var['g'],var['x'],var['y'],var['z'])]
  elif v[0]=='g':
    vd=[nonlinear.d5(var['a'],var['b'],var['g'],var['x'],var['y'],var['z'])]
#  vd=map(lambda x:parsedag(x,{},var),d)
##  print vd,vdq
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
    #tvf=parsedag(Fcu,{},var)
    tvf=nonlinear.delta(var['a'],var['b'],var['g'],var['x'],var['y'],var['z'])
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
#  if cu!=None: Fcu=curry(F,cu)
 # else: Fcu=F
#  vd=map(lambda x:parsedag(x,{},var),d)
  vd=[nonlinear.d1(var['a'],var['b'],var['g'],var['x'],var['y'],var['z']),
            nonlinear.d2(var['a'],var['b'],var['g'],var['x'],var['y'],var['z'])]

  sqrt=(reduce(lambda x,y:x+y,map(lambda (x,y):(x*y)**2,izip(vd,q))))**0.5
  p=map(lambda (x,y):x*y/sqrt,izip(vd,q))
  td={}
  dbg=False
  for e in var: td[e]=var[e]
  st=0.0
  dr=step[v]*10.0
  for (x,y) in izip(v,p): td[x]=var[x]-y*st
  #vst=parsedag(Fcu,{},td)
  vst=nonlinear.delta(td['a'],td['b'],td['g'],td['x'],td['y'],td['z'])
  for (x,y) in izip(v,p): td[x]=var[x]-y*dr
  #vdr=parsedag(Fcu,{},td)
  vdr=nonlinear.delta(td['a'],td['b'],td['g'],td['x'],td['y'],td['z'])
  dif=(dr-st)/10.0**5
  vmi=0
  while st+dif<dr:
    mi=(st+dr)/2.0
    for (x,y) in izip(v,p): td[x]=var[x]-y*mi
    vmi=nonlinear.delta(td['a'],td['b'],td['g'],td['x'],td['y'],td['z'])
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
	print("%.4f %.4f (%.4f) %.6f %.6f %.6f (%.6e) %f %d mode %d"%(var['y'],var['z'],step[('y','z')],var['a'],var['b'],var['g'],step[('a','b','g')],(vf),j,mode))

def minimize(F,dl,deltaList):
  mode=1
  var={'x':10000.0,'y':0.0,'z':0.0,'a':0.0,'b':0.00,'g':0.0} #synthetic1
  #var={'x':10000.0,'y':-3093.0,'z':6493.0,'a':-0.5,'b':-1.02,'g':-0.87} #livingroom-free1
  #var={'x':100.0,'y':15000.0,'z':0.0,'a':-0.4,'b':0.0,'g':0.0} #y-rotx
  #var={'x':10000.0,'y':-2962.9007,'z':4922.80,'a':-0.4106,'b':-0.9155,'g':-0.749} #points3/fence
  #var={'x':10000.0,'y':0.0,'z':0.0,'a':0.0,'b':-1.0,'g':0.0} 
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
  
      vf,pvf=optmxbin(F,(dl[1],dl[2]),var,('y','z'),vf,cu={'a':var['a'],'b':var['b'],'g':var['g'],'x':var['x']},stepup=2.0),vf
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
"""
    elif mode==3:
      if gdbg and dbgtime:
        print "mode 3 %d"%(clock()-tstart)
      vf,pvf=optmxbinall(F,(dl[1],dl[2],dl[3],dl[4],dl[5]),var,('y','z','a','b','g'),vf,stepup=2.0),vf
      if dbg and gdbg:
        printshit(var,vf,j,mode)
"""
def qstr(q):
  if q==qcos:    return 0 
  elif q==qsin:  return 1 
  elif q==qadd:  return 2
  elif q==qsub:  return 3 
  elif q==qmul:  return 4 
  elif q==qdiv:  return 5 
  elif q==qexp:  return 6 
  
def ptoc(x,dic,d={},fin={},vec={},index=[]):
  if isElement(x):
    if isinstance(x,(int,long,float)):
      if x not in fin:
        vec[index[0]]=(0,x)
        fin[x]=index[0] 
        index[0]+=1
      return fin[x] 
    elif isinstance(x,(basestring)):
      if x not in fin:
        vec[index[0]]=(0,x)
        fin[x]=index[0]
        index[0]+=1 
      return fin[x] 
    elif isinstance(x,(tuple)):
      if x[0] in op:
        if x not in fin:
          vec[index[0]]=(2,qstr(x[0]),str(ptoc(x[1],dic,d,fin,vec,index)),str(ptoc(x[2],dic,d,fin,vec,index)))
          fin[x]=index[0] 
          index[0]+=1
        return fin[x]
      if x[0] in func:
        if x not in fin:
          vec[index[0]]=(1,qstr(x[0]),ptoc(x[1],dic,d,fin,vec,index))
          fin[x]=index[0] 
          index[0]+=1 
        return fin[x] 
  elif isList(x):
    print "list"
  elif isMatrix(x):
    print "list"
def term(i):
  return "v["+str(i)+"]"

if __name__=="__main__":
  (p1,p2,s,f)=readfile("synthetic1.in")
  vecpic(p1,s,f)  
  (v1,v2)=map(lambda x:vecpic(x,s,f),[p1,p2])
  (F,dl,deltaList)=system(v1,v2) 
  vec={}
  fin={}
  index=[0]
  ptoc(dl[5],{},{},fin,vec,index)
  """
  for i in vec:
    s=term(i)+"="
    if vec[i][0]==0:
      s+=str(vec[i][1])
    elif vec[i][0]==1:
      if vec[i][1]==0:
        s+="cos("+term(vec[i][2])+")"
      elif vec[i][1]==1:
        s+="sin("+term(vec[i][2])+")"
    elif vec[i][0]==2:
      if vec[i][1]==2:
        s+=term(vec[i][2])+"+"+term(vec[i][3])
      if vec[i][1]==3:
        s+=term(vec[i][2])+"-"+term(vec[i][3])
      if vec[i][1]==4:
        s+=term(vec[i][2])+"*"+term(vec[i][3])
      if vec[i][1]==5:
        s+=term(vec[i][2])+"/"+term(vec[i][3])
      if vec[i][1]==6:
        s+="pow("+term(vec[i][2])+","+term(vec[i][3])+")"
    s+=";"
    print s
  """ 
      
  #for i in xrange(1000):
  #  parsedag(dl[3],{},{'a':1.0,'b':1.0,'g':1.0,'x':1.0,'y':1.0,'z':1.0})

  minimize(F,dl,deltaList)
  minimize([],[],[])
