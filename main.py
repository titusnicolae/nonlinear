#!/usr/bin/python
#from itertools import izip
from mat import * 
#from math import pi

if __name__=="__main__":
  m=[[1,2,5],[3,4,10],[44,55,12]]
  c=[3,90,33]
  print(map(nops,linsolve(tf(m),tf(c))))
