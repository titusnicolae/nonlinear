
#include <stdio.h>
#include "arbore.cpp"

int main ()
{  
  return 0;
}

void test1(int n)
{ double daux;
  double *r=new double[6];
  node *n=new node[6];
  FILE *fin=fopen("math.in","r");
  char *line=new char[200000];
  char *c,*aux;
  char var[]={"a","b","c","f","g","h","px","py","qx","qy"};
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
  
  FILE *f=fopen("test1.txt");
  for(int i=0;i<n;i++)
  { dict *d=new dict;
    printf("test suite %d",i);
    for (int j=0;j<10;j++)
    { fscanf(f,"%lf",&daux);
      dict.add(var[j],daux); 
    }
    for (int j=0;j<6;j++)
    { fscanf(f,"%lf",&daux);
      printf("it shoud be %lf; it's  %lf",daux,n[j]->evaluate(d)); 
    }

    printf("\n");
    delete d;
  }
}

double test2(node *n,double *d)
{ 
}
