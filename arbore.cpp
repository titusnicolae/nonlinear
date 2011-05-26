#include <string.h>
#include <stdio.h>
#include <vector>
using namespace std;
class node
{ bool isoperator;  //if it is a variable, or it's an operator 
  char *s;    //variable name or the name of the operator
  node *parent;    //parent
  vector<node*> list; //list of children
  public:
  node(bool isoperator, char *s)
  { this->isoperator=isoperator;
    this->s=s;
  }

  void addChild(node *p)
  { this->list.push_back(p);
    p->parent=this;
  }

  void print()
  { if(this->isoperator)
    { if(this->list.size()==1)
      { char *paren[2]={strdup(""),strdup("")};

        if(!strcmp("Cos",this->s) || !strcmp("Sin",this->s) || !strcmp("Abs",this->s))
        { paren[0]=strdup("[");
          paren[1]=strdup("]");  
        } 
        printf("%s%s",this->s,paren[0]);
        this->list[0]->print();
        printf("%s",paren[1]);
      }
      else if(this->list.size()>1)
      { char *paren[2]={strdup(""),strdup("")};

        if(node::priority(parent)>node::priority(this))
        { paren[0]=strdup("(");
          paren[1]=strdup(")"); 
        }
        printf("%s",paren[0]);    
       
        vector<node*>::const_iterator it=this->list.begin();
        ((node*)(*it))->print(); 
        for (++it;it!=this->list.end();++it)
        { printf("%s",this->s);
          ((node*)(*it))->print();  
        }
        printf("%s",paren[1]);
      }
    }
    else
    { printf("%s",this->s);
    }
  }
  static int priority(node *n)
  { if (n==NULL)
      return -1;
    if(!n->isoperator) 
      return 0;
    if(strcmp(n->s,"+")==0 || strcmp(n->s,"-")==0)
      return 1; 
    if(strcmp(n->s,"*")==0 || strcmp(n->s,"/")==0)
      return 2;
    return 3;
  }
  char* gets()
  { return s;
  }
};

/*
void process(char& *c)
{ node *p=NULL;
 
  while(c!=NULL)
  { 
    if(*c=='(' || *c=='[')
    {
    }
    else if(*c==')' || *c==']')
    {
    }
    else if(*c=='+')
    { 
    }
    else if(*c=='-')
    {
    }
    else if(*c=='/')
    {
    }
    else if(*c==' ') 
    {
    }
    else if(*c=='^')
    {
    }
    else if(*c>='A' && *c<='Z')
    {
    }
    else if(*c>='a' && *c<='z')
    { char str[10];int i=0; 
      while(*c>='a' && *c<='z')
        str[i++]=*(c++);
      str[i]=0;
      node *e=new node(true,NULL,strdup(str),NULL);
      if (p!=NULL)
      { 
        
      }  
    }
    else
    {  
    }
  }
  return r;
}
*/

int main ()
{ 
   
  char *line;
  FILE *fin=fopen("math.in","r");
  line=new char[140000];  
  fgets(line,140000,fin);
  node *a,*b,*c,*d,*e,*f;
  a=new node(true,strdup("Cos"));
  b=new node(false,strdup("u"));
  c=new node(true,strdup("+"));
  d=new node(false,strdup("2"));
  e=new node(true,strdup("*"));
  f=new node(false,strdup("something"));
  a->addChild(b);
  c->addChild(a);
  c->addChild(d);
  e->addChild(c);
  e->addChild(f);
  e->print(); 
  printf("\n");
  /*
  node *n[6];
  for (int i=0;i<6;i++)
  { c=strtok(line,"\n");
    while(c!=NULL)
    { printf("%s",c);
      //n[i]=process(c);
    } 
  }*/
  return 0;
}
