#include <string.h>
#include <stdio.h>
#include <vector>

using namespace std;
class node
{
private:
  bool isOperator;  //if it is a variable, or it's an operator 
  char *s;    //variable name or the name of the operator
  node *parent;    //parent

public:
  vector<node*> list; //list of children
  bool minus;
  bool inverse;

  node(bool isOperator, char *s,bool minus=false,bool inverse=false)
  { this->isOperator=isOperator;
    this->s=s;
    this->parent=NULL;
    this->minus=minus;
    this->inverse=inverse;
  }

  void addChild(node *p)
  { this->list.push_back(p);
    p->parent=this;
  }

  void print()
  {
    if(this->isOperator)
    { if(this->list.size()==1)
      { char *paren[2]={strdup(""),strdup("")};

        if(!strcmp("Cos",this->s) || !strcmp("Sin",this->s) || !strcmp("Abs",this->s))
        { paren[0]=strdup("[");
          paren[1]=strdup("]");  
        } 
        printf("%s%s",this->s,paren[0]);
        this->list[0]->print();
        printf("%s",paren[1]);
      
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
      return 0;
    if(n->isOperator) 
    { if(!strcmp(n->s,"+") || !strcmp(n->s,"-"))
        return 1; 
      if(!strcmp(n->s,"*") || !strcmp(n->s,"/"))
        return 2;
      if(!strcmp(n->s,"^"))
        return 3;
      if(!strcmp(n->s,"Sin") || !strcmp(n->s,"Cos") || !strcmp(n->s,"Abs"))
        return 4;
    }
    else 
      return 5;
  }

  char* gets()
  { return s;
  }

  bool getParent()
  { return this->parent;
  }

  bool hasParent()
  { if(this->p==NULL)
      return false;
    return true;
  }
  void updateSign(node *t)
  { this->minus^=t->getSign();
    t->setSign(false);
  }
  void setSign(bool flag)
  { this->minus=flag;
  }
  bool getSign()
  { return this->minus;
  }
  bool isOperand()
  { return !this->isOperator;
  }
};


node* process(char* &c,bool coa)
{ 
  node *p=NULL;//last operator or first operand
  char s1,s2,*func;
  bool wasminus=false;//todo dezactivare
  bool wasinverse=false;//la fel
  bool wasoperand=false;//daca ultima chestia a fost un operand

  while(c!=NULL)
  { 
    if(*c=='(' || *c=='[')
    { wasoperand=true;
      c++;
      node* r=process(c);
    }
    else if(*c==')' || *c==']')
    {
      c++;
      node *u=p;
      while(u->hasParent())
      { u=u->getParent();   
      } 
    }
    else if(*c=='+'||*c=='-')
    { 
      { 
        node *o=new node(true,strdup("+"));
        if(node::priority(p)==node::priority(o))//daca este sir de +-+-
        { c++; 
        }
        else //daca + trebuie pus deasupra de * sau ^
        { node *u=p;
          while(node::priority(o)<node::priority(u))
          { u=u->getParent();
          }
          if(node::priority(u)==node::priority(o))//era un + inainte de sirul ala de *
          { p=u;
            c++;
          }
          else//trebuie pus un + deasupra de * 
          { o.addChild(u); 
            o.updateSign(u); 
            p=o;
          }
        }
      }
      wasoperand=false;//trebuie la sfarsit neaparat!!
    }
    else if(*c==' '||*c=='/')
    { 
      wasoperand=false; 
      //creaza nod '*'
      if(p==NULL) printf("hopa penelopa");
      node *o=new node(true,strdup("*"));
      if(p->isOperand())
      { o.addChild(p);
        o.updateSign(p);
        p=o; 
      }
      else
      { if(node::priority(p)==node::priority(o))//e un sir de * 
        { c++; 
        }
        else if(node::priority(p)>node::priority(o)) //* trebuie pus deasupra de ^ si poate dedesubt de + 
        {   
          node *u=p;
          while(node::priority(u)>node::priority(o)&&u->hasParent())//urca de jos in sus pana ajunge la * sau sub *
          { u=u->getParent();                    
          }
          if (node::priority(u)==node::priority(o))//daca a ajuns la * dupa ce a urcat
          { p=u;
          }
          else //daca a ajuns sub * dupa ce a urcat
          { 
            if(u->hasParent())//daca exista + atunci
            { node* h=u->getParent();
              h->list.pop_back();
              h.addChild(o);
            }
            o.addChild(u); //* adauga pe ^ ca fiu
            o.updateSign(u); 
            p=o;
          }  
          c++; 
        }
        else //trebuie pus * sub + si furat de la + un termen
        { node *t=p->list.back();
          p->list.pop_back();
          p.addChild(o); 
          o.addChild(t);
          o.updateSign(t);
          p=o;
          c++;
        }
      }
    }
    else if(*c=='^')
    { wasoperand=false; 
    }
    else if((*c>=(s1='a') && *c<=(s2='z'))||(*c>=(s1='0') && *c<=(s2='9')))
    { 
      wasoperand=true; 
      char *t;
      for (t=c; *t>=s1 && *t<=s2;t++);
      char *s=new char[t-c+1]; //+1 pentru NULL
      strncpy(s,c,t-c);
      s[t-c]=0; //pune NULL la sfarsitul string-ului
      c=t;
      node *o=new node(false,s,wasminus,wasinverse);//nu e operator, baga sirul
      wasminus=wasinverse=false;
      if (p==NULL)
      { p=o;
      }    
      else
      { p.addChild(o);
      }
    }
    else if(!strncmp((func="Sin"),p,4) || !strncmp((func="Cos"),p,3) || !strncmp((func="Abs"),p,3))
    { wasoperand=true; 
    }
    else
    { printf("%c wtf is this shit",*c);
    }
  }
  return p;
}

void test()
{ node *a,*b,*c,*d,*e,*f;
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
}

int main ()
{ char *line,*c;
  FILE *fin=fopen("math2.in","r");
  line=new char[140000];  
  fgets(line,140000,fin);
  node *n[6];
  for (int i=0;i<1;i++)
  { c=strtok(line,"\n");
    while(c!=NULL)
    { printf("%s",c);
      n[i]=process(c);
      c=strtok(NULL,"\n");
    } 
  }
  return 0;
}

