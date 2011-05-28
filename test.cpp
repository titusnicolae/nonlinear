#include <string.h>
#include <stdio.h>
#include <vector>
using namespace std;
int main ()
{ char a[]="an";
  char b[]="ana are"; 
  printf("%d",strncmp(a,b,5));
  return 0;
}
