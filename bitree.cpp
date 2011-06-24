#include <stdio.h>
using namespace std;
typedef float num;
class Col
{ num el[3];
  
  public:
  Col(num a,num b,num c)
  {el[0]=a;el[1]=b;el[2]=c;
  }

  void print()
  { printf("%f %f %f",el[0],el[1],el[2]);
  }

  num operator[] (const unsigned& index)
  { return el[index];
  }

  Col operator+ ( Col other)
  { other.print(); 
    return Col(0,0,0);
  }
};

int main ()
{ Col a(1,2,3);
  Col b(1,2,3);
  Col c=a+b; 
  c.print();
  return 0;
}
