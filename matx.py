from itertools import izip
from math import sin,cos
#import psyco
#psyco.full()
def qadd(a,b):
  return a+b
def qsub(a,b):
  return a-b
def qmul(a,b):
  return a*b
def qdiv(a,b):
  return a/b
def qexp(a,b):
  return a**b 
def qsin(a):
  return sin(a)
def qcos(a):
  return cos(a)
op=(qmul,qdiv,qadd,qsub,qexp)
func=(qcos,qsin)

def dt(l,t):
  if isNumber(l):
    return 0
  elif isString(l):
    if l==t: return 1
    else: return 0
  elif isTuple(l): 
    if l[0] in op:
      if l[0]==qadd:
        if isNumber(l[1]): return dt(l[2],t)
        if isNumber(l[2]): return dt(l[1],t)   
        return (qadd,dt(l[1],t),dt(l[2],t))
      elif l[0]==qsub:
        if isNumber(l[2]): return dt(l[1],t)
        return (qsub,dt(l[1],t),dt(l[2],t))
      elif l[0]==qmul:
        if isNumber(l[1]): return (qmul,l[1],dt(l[2],t))
        if isNumber(l[2]): return (qmul,dt(l[1],t),l[2])
        return (qadd,(qmul,dt(l[1],t),l[2]),(qmul,l[1],dt(l[2],t)))
      elif l[0]==qdiv:
        return (qdiv,(qsub,(qmul,dt(l[1],t),l[2]),(qmul,l[1],dt(l[2],t))),(qexp,l[2],2))
      elif l[0]==qexp:
        if l[2]==2: return (qmul,2,(qmul,l[1],dt(l[1],t)))
        return (qmul,(qmul,l[2],(qexp,l[1],l[2]-1)),dt(l[1],t))
    
    elif l[0] in func:
      if l[0]==qsin:
        if l[1]==t: return (qcos,l[1])
        return 0 
      elif l[0]==qcos:
        if l[1]==t: return (qsub,0,(qsin,l[1]))
        return 0
    else:
      print("Error @ dt")
  elif isList(l):
    return map(lambda x:dt(x,t),l)
  else:
    print("Error2 @dt") 

def prunedag(l,dic):
  if isList(l):
    return map(lambda x:prunedag(x,dic),l)
  elif isTuple(l):
    if l[0] in op:
      a=prunedag(l[1],dic)
      b=prunedag(l[2],dic)
      if l[0]==qmul or l[0]==qadd:
        if (l[0],a,b) in dic:
          return dic[(l[0],a,b)]
        elif (l[0],b,a) in dic:
          return dic[(l[0],b,a)]
        else:
          dic[(l[0],a,b)]=(l[0],a,b)
          return dic[(l[0],a,b)]
      else:
        if (l[0],a,b) not in dic:
          dic[(l[0],a,b)]=(l[0],a,b)
        return dic[(l[0],a,b)]

    elif l[0] in func:
      a=prunedag(l[1],dic)
      if (l[0],a) not in dic:
        dic[(l[0],a)]=(l[0],a)
      return dic[(l[0],a)]

  elif isNumber(l) or isString(l):
    return l
  else:
    print("Error @ prunedag # type")
 
def curry(l,d):
  if isTuple(l):
    if l[0] in op:
      a=curry(l[1],d)
      b=curry(l[2],d)
      if isString(a) and a in d: a=d[a]
      if isString(b) and b in d: b=d[b]
      if isNumber(a,b):
        return l[0](a,b)
#        if l[0]==qmul: return a*b 
#        elif l[0]==qadd: return a+b 
#        elif l[0]==qsub: return a-b 
#        elif l[0]==qdiv: return a/b 
#        elif l[0]==qexp: return a**b
      else: return (l[0],a,b)
    elif l[0] in func:
      a=curry(l[1],d)
      if isString(a) and a in d: a=d[a]
      if isNumber(a):
        if l[0]==qsin: return sin(a)
        elif l[0]==qcos: return cos(a)
      else: return (l[0],a)
  elif isString(l):
    if l in d: return d[l]
    return l
  elif isNumber(l): return l
  elif isList(l):
    return map(lambda x:curry(x,d),l)
  print("Error @ curry")
      

def prune(l):
  if isList(l):
    return map(prune,l)
  elif isTuple(l):
    if l[0] in op:
      a=prune(l[1])
      b=prune(l[2])
      if l[0]==qadd:
        if isNumber(a,b): return a+b
        elif a==0: return b
        elif b==0: return a
        else: return (qadd,a,b)    
      elif l[0]==qsub:
        if isNumber(a,b): return a-b
        elif b==0: return a
        else: return (qsub,a,b)
      elif l[0]==qmul:
        if isNumber(a,b): return a*b
        elif a==0 or b==0: return 0
        elif a==1: return b
        elif b==1: return a
# elif isTuple(a,b) and l[1][0]==qsub and l[1][1]==' and l[2][0]==qsub and l[2][1]=='0':
      #    return (qmul,l[1][2],l[2][2])
        else: return (qmul,a,b)
      elif l[0]==qdiv: 
        if isNumber(a,b): return a/b
        elif a==0: return 0
        else: return (qdiv,a,b)
      elif l[0]==qexp:
        if isNumber(a,b):return a**b
        elif a==0: return 0
        elif b==1: return a
        else: return (qexp,a,b)
      else:
        print("Error @ prune # op")  
    elif l[0] in func:
      a=prune(l[1])
      if l[0]==qsin:
        if isNumber(a): return sin(a)
        else: return (qsin,a)
      elif l[0]==qcos:
        if isNumber(a): return cos(a)
        else: return (qcos,a)
  elif isNumber(l) or isString(l):
    return l
  else:
    print("Error @ prune # type")    


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

def isTuple(*x):
  return true(map(lambda x:isinstance(x,tuple),x))

def isNumber(*x):
  return true(map(lambda x:isinstance(x,(int,float,long)),x))

def isString(x):
  return isinstance(x,basestring)

def isElement(*x):
  return true(map(lambda x:isinstance(x,(int,float,long,tuple,basestring)),x))

def isList(*x):
  return true(map(lambda x:isinstance(x,list) and not isinstance(x[0],list),x))

def isMatrix(x):
  return isinstance(x,list) and isinstance(x[0],list)

def csum(a,b):
  if isElement(a,b): 
    return (qadd,a,b)
  elif isList(a) and isList(b):
    return [(qadd,x,y) for x,y in izip(a,b)]
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
  return reduce(lambda x,y: (qadd,x,y),
                [(qmul,par(i),(qmul,m[i][0],det(subm(m,i)))) for (i,l) in enumerate(m)])

def rc(m,c,p): #replace with column c in matrix m at position p
  r=[]
  for (i,e) in enumerate(m):
    if i==p:
      r.append(c)
    else:
      r.append(e)
  return r 

def linsolve(m,c): 
#  r=[]
#  d=det(m)
#  for (i,e) in enumerate(m):
#    r.append(div(det(rc(m,c,i)),d))
#  return r
  return div(det(rc(m,c,2)),det(m))
 
def f(x): #tofloat
  if isMatrix(x):
    return [(lambda l:map(float,l))(l) for l in x]
  if isList(x):
    return map(float,x)
  if isinstance(x,(int,long)):
    return float(x)

def cross(a,b):
  if isList(a,b):
    t=map(list,zip(a,b))
    return [det(t[1:]),minus(det([t[0],t[2]])),det(t[:2])] 
      
  else:
    print("Error @ cross") 

def sub(a,b):
  if isElement(a,b):
    return (qsub,a,b)
  elif isList(a,b):
    return map(lambda (x,y):(qsub,x,y),izip(a,b))
  else:
    print "Error @ sub" 

def minus(a):
  if isElement(a):
    return (qsub,0,a) 
  elif isList(a):
    return map(lambda x:(qsub,0,x),a)
  else:
    print "Error @ minus" 
       
def add(a,b):
  if isElement(a,b):
    return (qadd,a,b)
  elif isList(a,b):
    return map(lambda (x,y):(qadd,x,y),izip(a,b)) 
  else:
    print "Error @add" 
 
def div(a,b):
  if isElement(a,b):
    return (qdiv,a,b)
  else:
    print "Error @ div!"
  
def mul(a,b):
  if isElement(a): 
    if isElement(b):
      return (qmul,a,b)
    elif isList(b):
      return [(qmul,a,x) for x in b]
    elif isMatrix(b):
      return [[(qmul,a,x) for x in c ] for c in b] 

  elif isList(a):
    if isElement(b):
      return [(qmul,b,x) for x in a]
    elif isList(b):
      return reduce(lambda x,y:(qadd,x,y),[(qmul,x,y) for (x,y) in izip(a,b)])
    elif isMatrix(b):
      return "wtf"

  elif isMatrix(a):
    if isElement(b):
      return [[(qmul,b,x) for x in c ] for c in a] 
    elif isList(b):
      return [mul(b,c) for c in map(list,zip(*a))]
    elif isMatrix(b):
      return [[mul(c,d) for c in map(list,zip(*a))] for d in b]

def sq(a):
  if isList(a):
    return reduce(lambda x,y:(qadd,x,y),[(qexp,x,2) for x in a])
  if isElement(a):
    return (qexp,a,2) 
  else:
    print "crap on a spatula"
   

def id():
  return [[1,0,0],[0,1,0],[0,0,1]]

def transpose(m):
  r=[[]]*3
  for i in range(0,3):
    for j in range(0,3):
      r[j].append(m[i][j])
  return r

def parsedag(x,dic,d=None):
  if isElement(x):
    if isinstance(x,(int,long,float)):
      return x
    elif isinstance(x,(basestring)):
      if not x in d: print "crap"
      return d[x]
    elif isinstance(x,(tuple)):
      if x[0] in op:
        if x not in dic:
          a=parsedag(x[1],dic,d)
          b=parsedag(x[2],dic,d)
          dic[x]=x[0](a,b)
#          if x[0]==qmul: dic[x]=a*b 
#          elif x[0]==qadd: dic[x]=a+b 
#          elif x[0]==qsub: dic[x]=a-b 
#          elif x[0]==qdiv: dic[x]=a/b 
#          elif x[0]==qexp: dic[x]=a**b
        return dic[x]
      if x[0] in func:
        if x not in dic:
          a=parsedag(x[1],dic,d)       
          dic[x]=x[0](a) 
#          if x[0]==qsin:   dic[x]=sin(a)
#          elif x[0]==qcos: dic[x]=cos(a)
        return dic[x]
  elif isList(x):
    return [parsedag(e,dic,d) for e in x]   
  elif isMatrix(x):
    return [[parsedag(e,dic,d) for e in c] for c in x] 
 
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
        return x[0](a,b)
#        if x[0]==qmul: return a*b 
#        elif x[0]==qadd: return a+b 
#        elif x[0]==qsub: return a-b 
#        elif x[0]==qdiv: return a/b 
#        elif x[0]==qexp: return a**b
      if x[0] in func:
        a=parse(x[1],d)
#        if x[0]==qsin:   return sin(a)
#        elif x[0]==qcos: return cos(a)
        return x[0](a)
  elif isList(x):
    return [parse(e,d) for e in x]   
  elif isMatrix(x):
    return [[parse(e,d) for e in c] for c in x] 
 
def nops (x):
  if isElement(x):
    if isinstance(x,(int,long,float,basestring)):
      return 0
    elif isinstance(x,tuple):
      if x[0] in op:
        return 1+nops(x[1])+nops(x[2])
      elif x[0] in func:
        return 1+nops(x[1])
  elif isList(x):
    return reduce(lambda x,y:x+y,map(nops,x)) 
  elif isMatrix(x):
    s=0
    for c in x:
      for e in c:
        s+=nops(e)
    return s
  else:
    print "Error @ nops"   


def Sin(a):
  return (qsin,a)

def Cos(a):
  return (qcos,a)

def rot(a,b,g):
  ra=[[1,0,0],
      [0,Cos(a),Sin(a)],
      [0,minus(Sin(a)),Cos(a)]]
  rb=[[Cos(b),0,minus(Sin(b))],
      [0,1,0],
      [Sin(b),0,Cos(b)]]
  rg=[[Cos(g),Sin(g),0],
      [minus(Sin(g)),Cos(g),0],
      [0,0,1]] 
  return mul(ra,mul(rb,rg))

def intersect(u,v,s):
  return linsolve([u,v,cross(u,v)],s)

def delta(u,v,s,r):
  p=intersect(u,mul(rot(*r),v),s) 
#  p=intersect(u,v,s) 
#  return sq(sub(sub(mul(p[0],u),s),mul(p[1],mul(rot(*r),v))))
  return mul(sq(cross(u,mul(rot(*r),v))),sq(p))

