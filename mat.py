from itertools import izip
def isElement(x):
  return isinstance(x,(int,float,long,tuple,basestring))
def isList(x):
  return isinstance(x,list) and not isinstance(x[0],list)
def isMatrix(x):
  return isinstance(x,list) and isinstance(x[0],list)

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
      return [mul(b,c) for c in a]
    elif isMatrix(b):
      return [[mul(c,d) for c in a] for d in b]

