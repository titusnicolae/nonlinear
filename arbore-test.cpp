#include <stdio.h>
#include "arbore.cpp"
void test1(int);

int main ()
{ test1(1); 
  return 0;
}

void test1(int k)
{ 
  long double daux;
  long double *r=new long double[6];
  node *n[6];
  FILE *fin=fopen("math.txt","r");
  char *line=new char[200000];
  char *c,*aux;
  char var[][8]={"a","b","g","f","qx","qy","h","v","offsetx","offsety","px","py"};
  dict *d=new dict;
  int i=0; 
  fread(line,200000,1,fin);
  c=strtok(line,"\n");
  while(c!=NULL)
  { aux=c;
    n[i]=process(aux);
    i++;
    c=strtok(NULL,"\n");  
  }  
  //there better be 6 expressions in that file!!  
  
  FILE *f=fopen("test2.txt","r");
  for(int i=0;i<k;i++)
  { dict *d=new dict;
    printf("test suite %d",i);
    for (int j=0;j<12;j++)
    { fscanf(f,"%Lf",&daux);
      d->add(var[j],daux); 
    }
    for (int j=0;j<6;j++)
    { fscanf(f,"%Lf",&daux);
      printf("it shoud be %Le; it's  %Le\n",daux,n[j]->evaluate(d)); 
    }
    printf("\n");
    delete d;
  }
}

