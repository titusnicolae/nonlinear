#!/usr/bin/python
a=[[1,2,3],[4,5,6],[7,8,9]]
def subm(m,k):
  r=[]
  for (i,l) in enumerate(m):
    if i==k: continue
    r.append(l[1:])
  return r

print(subm(a,1))
