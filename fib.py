#!/usr/bin/python
from mat import *
#l=[T(('+',1,1)),T(('+',1,0))]
l1=[('+',1,1),('+',1,0)]
l2=[('+',1,1),('+',1,0)]
for i in range(2,1000000):
#  l.append(T(('+',l[i-1],l[i-2])))
  l1.append(('+',l1[i-1],l1[i-2]))
  l2.append(('+',l2[i-1],l2[i-2]))

t1=l1[len(l1)-1]
t2=l2[len(l2)-2]
a=('+',t1,t1)
b=('+',t2,t2)
print a==b 





