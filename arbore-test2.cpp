#include "arbore.cpp"
#include <string.h>
#include <stdio.h>

int main ()
{ 
  FILE *f=fopen("math2.in","r");
  char *text=new char[1000];
  fread(text,1000,1,f);
  node *n[100];
  int i=0;
  dict *d=new dict;
  d->add(strdup("pi"),3.141);
  char *c=strtok(text,"\n"),*aux;
  while(c!=NULL)
  { aux=c;
    n[i]=process(aux);
    n[i]->print();
    printf("\n"); 
    i++;
    c=strtok(NULL,"\n"); 
  }
  for (int j=0;j<i;j++)
  { printf("%lf\n",n[j]->evaluate(d));  
  }
   
  return 0;
}
