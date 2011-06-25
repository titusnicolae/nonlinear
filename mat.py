from itertools import izip
from math import sin,cos
op=("*","/","+","-","^")
func=("cos","sin")

def dt(l,t):
  if l[0] in op:
    if l[0]=="+" or l[0]=="-":
      return ("+",dt(l[1],t),dt(l[2],t))
    elif l[0]=="*": 
      return ("+",("*",dt(l[1],t),l[2]),("*",l[1],dt(l[2],t)))
    elif l[0]=="/":
      return ("/",("-",("*",dt(l[1],t),l[2]),("*",l[1],dt(l[2],t))),("^",l[2],2))
    elif l[0]=="^":
      return ("*",("*",l[2],("^",l[1],l[2]-1)),dt(l[1],t))
  
  elif l[0] in func:
    if l[0]=="sin":
      return ("*",("cos",l[1]),dt(l[1],t))  
    elif l[0]=="cos":
      return ("*",
              ("*",-1,("sin",l[1])),
              dt(l[1],t)
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

def true(l):
  return reduce(lambda a,b:a and b,l)

def isElement(*x):
  return true(map(lambda x:isinstance(x,(int,float,long,tuple,basestring)),x))

def isList(x):
  return isinstance(x,list) and not isinstance(x[0],list)

def isMatrix(x):
  return isinstance(x,list) and isinstance(x[0],list)

def csum(a,b):
  if isElement(a,b): 
    return ("+",a,b)
  elif isList(a) and isList(b):
    return [("+",x,y) for x,y in izip(a,b)]
  else:
    print("shit")

def par(k):
  if k%2:
    return -1
  else:
    return 1 

def subm(m,k):
  r=[]
  for (i,l) in enumerate(m):
    if i==k: continue
    r.append(l[1:])
  return r 
   
def det(m):
  if len(m)==1:
    return m[0][0] 
  return reduce(lambda x,y: ("+",x,y),
                [("*",par(i),("*",m[i][0],det(subm(m,i)))) for (i,l) in enumerate(m)])

def rc(m,c,p): #replace with column c in matrix m at position p
  r=[]
  for (i,e) in enumerate(m):
    if i==p:
      r.append(c)
    else:
      r.append(e)
  return r 

def linsolve(m,c): 
  r=[]
  d=det(m)
  for (i,e) in enumerate(m):
    r.append(div(det(rc(m,c,i)),d))
  return r
 
def tf(x): #tofloat
  if isMatrix(x):
    return [(lambda l:map(float,l))(l) for l in x]
  if isList(x):
    return map(float,x)
  if isinstance(x,(int,long)):
    return float(x)

def sub(a,b):
  if isElement(a,b):
    return ("-",a,b)
  else:
    print "Error @ sub" 
 
def div(a,b):
  if isElement(a,b):
    return ("/",a,b)
  else:
    print "Error @ div!"
  
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
 
def nops(x):
  if isElement(x):
    if isinstance(x,(int,long,float,basestring)):
      return 0
    elif isinstance(x,tuple):
      if x[0] in op:
        return 1+nops(x[1])+nops(x[2])
      elif x[0] in func:
        return 1+nops(x[1])
  else:
    print "cmon"   

#def intersect(u,v,s):
#  b=div(,)
  
  
   
      
