#include <stdio.h>
int main ()
{ char s[]="ana are 123 mere si ce daca";
  char *c;
  for (c=s; !(*c>='0' && *c <='9');c++);
  char *p;
  for (p=c; *p>='0' && *p<='9';p++);
  printf("%d",p-c); 
  return 0;
}
