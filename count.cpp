#include <stdio.h>
#include <string.h>
int main ()
{ FILE *f=fopen("math.txt","r");
  char line[100000];
  for (int i=0;i<6;i++)
  { fgets(line,100000,f);
    printf("%d\n",strlen(line));
  }
  return 0; 
}
