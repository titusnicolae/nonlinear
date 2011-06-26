#!/usr/bin/python
from random import randint
from math import cos
class M:
  def __init__(self):
    self.dcos={}

  def cos(self,x):
    if x in self.dcos:
      return self.dcos[x]
    else:
      return self.dcos[x]=cos(x)
      return self.dcos[x]

if __name__=="__main__":
  m=M()
  for i in range(1,3000000):
#    x=cos(randint(0,6))   
    x=m.cos(randint(0,6))
  

