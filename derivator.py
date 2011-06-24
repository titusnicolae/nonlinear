#!/usr/bin/python
from sys import stdout
op=("*","/","+","-","^")
func=("cos","sin")
def d(l,t):
  if l[0] in op:
    if l[0]=="+" or l[0]=="-":
      return ("+",d(l[1],t),d(l[2],t))
    elif l[0]=="*": 
      return ("+",("*",d(l[1],t),l[2]),("*",l[1],d(l[2],t)))
    elif l[0]=="/":
      return ("/",("-",("*",d(l[1],t),l[2]),("*",l[1],d(l[2],t))),("^",l[2],2))
    elif l[0]=="^":
      return ("*",("*",l[2],("^",l[1],l[2]-1)),d(l[1],t))
  elif l[0] in func:
    if l[0]=="sin":
      return ("*",("cos",l[1]),d(l[1],t))  
    elif l[0]=="cos":
      return ("*",
              ("*",-1,("sin",l[1])),
              d(l[1],t)
             ) 
  else:
    if l[0]==t:
      return 1
    else:
      return 0  

def pr(l):
  r=""
  if not isinstance(l,(tuple)):
    r+=str(l)
     
  elif l[0] in op:
    r+="("+pr(l[1])
    if isinstance(l[0],(int,long,float)): r+=str(l[0])
    else: r+=l[0]
    r+=pr(l[2])+")"

  elif l[0] in func:
    r+=l[0]+"("
    r+=pr(l[1])
    r+=")"
  return r

if __name__=="__main__":
  t=("*","a","a")
  stdout.write(pr(d(t,"a"))+"\n")
