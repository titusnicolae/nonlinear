#include <stdio.h>
#include <string.h>
#include <vector>
using namespace std;
class C
{ 
private:
  int a;
public:
  C(int x)
  {a=x;
  }

  int get()
  { return a;
  }

};

int main ()
{ vector<C> v;
  for (int i=0;i<10;i++)
  { v.push_back(i);
  }

  for (int i=0;i<10;i++)
  { printf("%d ",v[i].get());
  }
  printf("\n"); 
  for (vector<C>::iterator it=v.begin();it!=v.end();++it)
  { printf("%d ",it->get()); 
  } 
  return 0;
}
