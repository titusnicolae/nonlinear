#!/usr/bin/python2.6
import psyco
#psyco.full()
def f():
  for i in xrange(1,100000000):
    x=i*2

if __name__=="__main__":
  f()
   
