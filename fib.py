#!/usr/bin/python
fib=[1,1]
for i in range(2,1000000):
  fib.append(("+",fib[i-1],fib[i-2]))

def compute(
