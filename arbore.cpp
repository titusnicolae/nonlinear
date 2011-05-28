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
  
  void print(bool first)
  { char* func;
    char cos[]="Cos[",sin[]="Sin[",abs[]="Abs[";

    if(this->isOperator)
    { vector<node*>::const_iterator it=this->list.begin();
      if(node::priority(this)==1)
      { for (;it!=this->list.end();++it)
        { (*it)->print(it==this->list.begin());
        }
      }
      else if(node::priority(this)==2)
      { printf("%s",this->minus?"-":(first?"":"+"));
        this->list[0]->print(true);
        for (++it;it!=this->list.end();++it)
        { if(node::priority(this)==2)
          { printf("%c",(*it)->inverse?'/':'*');
          }
          (*it)->print(true);  
        }
      }
      else if(node::priority(this)==3)
      { 
        this->list[0]->print(first);
        printf("^");
        this->list[1]->print(true);
      }
    }
    else
    { if(!strcmp(func=cos,this->s) || !strcmp(func=sin,this->s) || !strcmp(func=abs,this->s))
      { 
        printf("%s",this->minus?"-":(first?"":"+"));
        printf("%s",func);
        this->list[0]->print(first);
        printf("]");
      }
      else if(!strcmp("(",this->s))
      { 
        printf("%s(",this->minus?"-":(first?"":"+"));
        this->list[0]->print(first);
        printf(")");
      }
      else
      { printf("%s%s",this->minus?"-":(first?"":"+"),this->s);
      }
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

  void addChild(node *p)
  { this->list.push_back(p);
    p->parent=this;
  }

  node* getParent()
  { return this->parent;
  }

  bool hasParent()
  { if(this->parent==NULL)
      return false;
    return true;
  }
  void updateSign(node *t)
  { this->minus^=t->getSign();
    t->minus=false;
  }
  void updateSign(bool flag)
  { this->minus^=flag;
  }
  void updateInverse(bool flag)
  { this->inverse=flag;
  }
  bool getSign()
  { return this->minus;
  }
  bool isOperand()
  { return !this->isOperator;
  }
};

node* process(char* &c)
{ 
  node *p=NULL;//last operator or first operand
  char s1,s2,*func;
  bool wasminus=false;//todo dezactivare
  bool wasinverse=false;//la fel
  bool wasoperand=false;//daca ultima chestia a fost un operand
  char cos[]="Cos[",sin[]="Sin[",abs[]="Abs[";
  while(*c!='\0')
  { 
    if(*c=='(')
    { wasoperand=true;
      c++;
      node *o=new node(false,strdup("("),wasminus,wasinverse);
   

      printf("**%c%s\n",wasminus?'-':'+',"(");

 
      node* r=process(c);
      o->addChild(r);
      if(p==NULL)
      { p=o;
      }
      else
      { p->addChild(o);
        if(node::priority(p)==2)
          p->updateSign(o);
      } 
      wasminus=wasinverse=false;
    }
    else if(*c==')' || *c==']')
    {
      c++;
      node *u=p;
      while(u->hasParent())
      { u=u->getParent();   
      }
      return u; 
    }
    else if(*c=='+'||*c=='-')
    { wasminus=(*c=='-');
      c++;
      if(wasoperand)
      { node *o=new node(true,strdup("+"));
        if(p->isOperand())
        { 
          o->addChild(p); 
          p=o;
        }
        else
        { 
          if(node::priority(p)==node::priority(o))//daca este sir de +-+-
          { 
          }
          else //daca + trebuie pus deasupra de * sau ^
          { node *u=p;
            while(u->hasParent())//better be right
            { u=u->getParent();
            }
            if(node::priority(u)==node::priority(o))//era un + inainte de sirul ala de *
            { p=u;
            }
            else//trebuie pus un + deasupra de * 
            { o->addChild(u); 
              p=o;
            }
          }
        }
      }
      wasoperand=false; //trebuie la sfarsit neaparat!!
    }
    else if(*c==' '||*c=='*'||*c=='/')
    { wasinverse=(*c=='/');
      c++;
      //creaza nod '*'
      if(p==NULL) printf("hopa penelopa");
      node *o=new node(true,strdup("*"));

      if(p->isOperand())
      { o->addChild(p);
        o->updateSign(p);
        p=o; 
      }
      else
      { if(node::priority(p)==node::priority(o))//e un sir de * 
        { 
        }
        else if(node::priority(p)>node::priority(o)) //* trebuie pus deasupra de ^ si poate dedesubt de + 
        {   
          node *u=p;
          while(u->hasParent()&&node::priority(u->getParent())>=node::priority(o))//urca de jos in sus pana ajunge la * sau sub *
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
              h->addChild(o);
            }
            o->addChild(u); //* adauga pe ^ ca fiu
            o->updateSign(u); //(no inverse) 
            p=o;
          }  
        }
        else //trebuie pus * sub + si furat de la + un termen
        { 
          node *t=p->list.back();
          p->list.pop_back();
          p->addChild(o); 
          o->addChild(t);
          o->updateSign(t);
          p=o;
        }
      }
      wasoperand=false; 
    }
    else if(*c=='^')
    { c++;
      node *o=new node(true,strdup("^"));
      if(p->isOperand())
      { o->addChild(p);
        o->updateSign(p);
        p=o;  
      }
      else if(node::priority(p)<=3) // a+b^2 a*b^2 a^2^2
      { node *t=p->list.back();
        p->list.pop_back();
        p->addChild(o);
        o->addChild(t);
        o->updateSign(t);
        p=o; 
      }
      wasoperand=false;
    }
    else if((*c>=(s1='a') && *c<=(s2='z'))||(*c>=(s1='0') && *c<=(s2='9')))
    { 
      char *t;
      for (t=c; *t>=s1 && *t<=s2;t++);
      char *s=new char[t-c+1]; //+1 pentru NULL
      strncpy(s,c,t-c);
      printf("**%c%s\n",wasminus?'-':'+',s);
      s[t-c]=0; //pune NULL la sfarsitul string-ului
      c=t;
      //////
      node *o=new node(false,s,wasminus,wasinverse);
      
      if (p==NULL)
      { p=o;
      }    
      else
      { p->addChild(o);
        if(node::priority(p)==2)
        { p->updateSign(o);
        }
      }
      //////

      wasoperand=true; 
      wasminus=wasinverse=false;
    }
    else if(!strncmp((func=sin),c,4) || !strncmp((func=cos),c,4) || !strncmp((func=abs),c,4))
    { 
      c+=strlen(func);
      node *o=new node(false,strdup(func),wasminus,wasinverse);
      node *r=process(c);
      o->addChild(r); 
         
      if(p!=NULL)
      { p->addChild(o);
        if(node::priority(p)==2)
        { p->updateSign(o);  
        }         
      }
      else
      { p=o;  
      }
      wasoperand=true;
      wasminus=wasinverse=false; 
    }
    else
    { printf("%d%c wtf is this shit",*c,*c);
      return p;
    }
  }
 
  node *u=p;
  while(u->hasParent())
  { u=u->getParent();   
  }
  return u; 
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
  e->print(true); 
  printf("\n");
}

int main ()
{ char *line,*c;
  char *aux;
  FILE *fin=fopen("math2.in","r");
  line=new char[140000];  
  fread(line,140000,1,fin);
  int i=0;
  node *n[6];
  c=strtok(line,"\n");
  while(c!=NULL)
  { 
    printf("%s\n",c);
    aux=c;
    n[i]=process(aux);
    n[i++]->print(true);
    printf("\n\n");
    c=strtok(NULL,"\n");
  }
  return 0;
}
