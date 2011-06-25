from itertools import izip
from math import sin,cos
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


def isElement(x):
  return isinstance(x,(int,float,long,tuple,basestring))
def isList(x):
  return isinstance(x,list) and not isinstance(x[0],list)
def isMatrix(x):
  return isinstance(x,list) and isinstance(x[0],list)
#def csum(a,b):
#  if isList(a) and isList(b):
#    return [("+",x,y) for x,y in izip(a,b)]
#  else:
#    print("shit")
 
def mul(a,b):
  if isElement(a): 
    if isElement(b):
      return ("*",a,b)
    elif isList(b):
      return [("*",a,x) for x in b]
    elif isMatrix(b):
      return [[("*",a,x) for x in c ] for c in b] 

  elif isList(a):
    if isElement(b):
      return [("*",b,x) for x in a]
    elif isList(b):
      return reduce(lambda x,y:("+",x,y),[("*",x,y) for (x,y) in izip(a,b)])
    elif isMatrix(b):
      return "wtf"

  elif isMatrix(a):
    if isElement(b):
      return [[("*",b,x) for x in c ] for c in a] 
    elif isList(b):
      return [mul(b,c) for c in zip(*a)]
    elif isMatrix(b):
      return [[mul(c,d) for c in a] for d in b]

def id():
  return [[1,0,0],[0,1,0],[0,0,1]]

def transpose(m):
  r=[[]]*3
  for i in range(0,3):
    for j in range(0,3):
      r[j].append(m[i][j])
  return r
 
def parse(x,d=None):
  if isElement(x):
    if isinstance(x,(int,long,float)):
      return x
    elif isinstance(x,(basestring)):
      if not x in d: print "crap"
      return d[x]
    elif isinstance(x,(tuple)):
      if x[0] in op:
        a=parse(x[1],d)
        b=parse(x[2],d)
        if x[0]=="+":   return a+b 
        elif x[0]=="-": return a-b 
        elif x[0]=="*": return a*b 
        elif x[0]=='/': return a/b 
        elif x[0]=='^': return a**b
      if x[0] in func:
        a=parse(x[1],d)
        if x[0]=="sin":   return sin(a)
        elif x[0]=="cos": return cos(a)
  elif isList(x):
    return [parse(e,d) for e in x]   
  elif isMatrix(x):
    return [[parse(e,d) for e in c] for c in x] 
  
