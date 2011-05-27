#include <stdio.h>
#include <vector>
using namespace std;
int main ()
{ vector<int> a;
  for(int i=0;i<10;i++)
  { a.push_back(i);
  }
  for (int i=0;i<a.size();i++) 
    printf("%d",a[i]);
  printf("%d",a.back());
  a.pop_back();
  printf("\n");
  for (int i=0;i<a.size();i++)
  { printf("%d",a[i]);
  }
  return 0;
}
