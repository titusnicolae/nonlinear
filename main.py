#!/usr/bin/python
#from itertools import izip
from mat import * 
#from math import pi
from random import random
def genRandomDict(*args):
  r={}
  for l in args:
    for e in l:
      r[e]=random()*100 
  return r  

 
if __name__=="__main__":  
  r=['a','b','g']
  u=['ux','uy','uz']
  v=['vx','vy','vz']
  s=['sx','sy','sz']
  step=0.1
  var=genRandomDict(r,u,v,s) 
  d=delta(u,v,s,r)
  da=prune(dt(d,'a'))
  db=prune(dt(d,'b'))
  dg=prune(dt(d,'g'))
  dx=prune(dt(d,'sx'))
  dy=prune(dt(d,'sy'))
  dz=prune(dt(d,'sz'))
  
  vd=parse(d,var)      
  vda=parse(da,var)      
  vdb=parse(db,var)      
  vdg=parse(dg,var)      
  vdx=parse(dx,var)      
  vdy=parse(dy,var)      
  vdz=parse(dz,var)

  print("%.6f %.6f %.6f %.6f %.6f %.6f %.6f " % (vd,vda,vdb,vdg,vdx,vdy,vdz)) 
  for i in range(1,200):
    vd=parse(d,var)      
    vda=parse(da,var)      
    vdb=parse(db,var)      
    vdg=parse(dg,var)      
    vdx=parse(dx,var)      
    vdy=parse(dy,var)      
    vdz=parse(dz,var)
    if vda>0: var['a']+=step
    else: var['a']-=step
    if vdb>0: var['b']+=step
    else: var['b']-=step
    if vdg>0: var['g']+=step
    else: var['g']-=step
    if vdx>0: var['sx']+=step
    else: var['sx']-=step
    if vdy>0: var['sy']+=step
    else: var['sy']-=step
    if vdz>0: var['sz']+=step
    else: var['sz']-=step
    print("%.6f %.6f %.6f %.6f %.6f %.6f %.6f " % (vd,vda,vdb,vdg,vdx,vdy,vdz))
    if i%50==0: step=step/10.0
