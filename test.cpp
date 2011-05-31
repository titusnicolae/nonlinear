#include <math.h>
#include <stdio.h>
int main ()
{ int i;
  long double d;
  for (i=0,d=1.0;i<(1<<20);i++)
  { d*=2.0;
    printf("%lle %d\n",d,isinf(d));
    if(isinf(d))
      break;
  }
  return 0;
}
