#!/usr/bin/python
import sys
def median(l):
  s=0.0
  for e in l:
    s+=e
  return s/len(l)

def st_dev(l):
  u=median(l)
  s=0.0
  for e in l:
    s+=(e-u)**2
  s/=len(l)
  return s**0.5

def prelucrare():
  if len(sys.argv)<2:
    print "fisier de intrare lipsa" 
    return
  f=open(sys.argv[1],"r")
  l=[]
  for (i,line) in enumerate(f):  
    if i%3==0 and i>0:
      if len(line.split())>7: 
        l.append(float(line.split()[7]))
  print "median    %f"%(median(l))  
  print "deviation %f"%(st_dev(l))
 
if __name__=="__main__":
  prelucrare()
