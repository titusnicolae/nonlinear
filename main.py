#!/usr/bin/python
#from itertools import izip
from mat import * 
#from math import pi




if __name__=="__main__":  
  r=['a','b','g']
  u=['ux','uy','uz']
  v=['vx','vy','vz']
  s=['sx','sy','sz']
  d=delta(u,v,s,r)
  print(nops(dt(d,"a")))
  print(nops(prune(dt(d,"a"))))


