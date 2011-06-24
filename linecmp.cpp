#include <utility>
#include <vector>
#include <string.h>
#include <stdio.h>
#define N 100000
using namespace std;

char line1[N],line2[N];
int i1[N],i2[N];
int *p1=i1,*p2=i2,*aux;

int main ()
{ 
/*FILE *fiesire=fopen("iesire.txt","r");
  FILE *fmath=fopen("math.txt","r");*/
  FILE *fiesire=fopen("fisier1","r");
  FILE *fmath=fopen("fisier2","r"); 

  FILE *html=fopen("html.html","w");
  int i,j,k,l1,l2,max;
  vector<pair<int,int> >v[N];
  pair<int,int> p;
  vector<pair<int,int> >r; 
   
  for (int i=0;i<1;i++)
  { fgets(line1+1,N,fiesire); 
    fgets(line2+1,N,fmath);
    l1=strlen(line1+1);
    l2=strlen(line2+1);
    printf("%d %d\n",l1,l2); 
    
    memset(p1,0,(l2+1)*sizeof(int));
    memset(p2,0,(l2+1)*sizeof(int));
    max=0;
    for (j=1;j<=l1;j++)
    { for (k=1;k<=l2;k++)
      { if(line1[j]==line2[k])
        { p2[k]=p1[k-1]+1;
          v[p2[k]].push_back(make_pair(j,k));
          if(max<p2[k])
            max=p2[k];
        }
        else
        { p2[k]=p1[k]>p2[k-1]?p1[k]:p2[k-1];
        } 
      }
      aux=p1;
      p1=p2;
      p2=aux;
      memset(p2,0,l2+1);
    }
    p=v[max][0];

    r.push_back(p);
    for (j=max-1;j>=1;j--)
    { for (k=0;k<v[j].size();k++)
      { if(v[j][k].first<p.first&&v[j][k].second<p.second)  
        { p=v[j][k];  
          r.push_back(p);
          break;
        }
      } 
    }
    for (vector<pair<int,int> >::const_iterator it=r.begin();it!=r.end();++it)
    { fprintf(html,"%d %d\n",it->first,it->second);
    }
    char *out1=new char[100000];
    char *out2=new char[100000];
    memset(out1,0,100000);
    memset(out1,0,100000);
    int o1=0,o2=0;
    
    char *c1=out1,*c2=out2,*cl1=line1,*cl2=line2;
    pair<int,int> prev=*(r.rbegin());

    for (vector<pair<int,int> >::reverse_iterator rit=r.rbegin()+1;rit!=r.rend();++rit)
    { 
      for (int j=prev.first;j<rit->first;j++)
      { c1[j+o1]=out1[j];
      }
      for (int k=prev.second;k<rit->second;k++)
      { c2[k+o2]=out2[k];
      }
      if(rit->second-prev.second>rit->first-prev.first)
      { o1+=(rit->second-prev.second)-(rit->first-prev.first);
      }
      else
      { o2+=(rit->second-prev.second)-(rit->first-prev.first);
      } 
      o1+=;
      o2+=;
      prev=*rit;
    }  
 
    fprintf(html,"%s\n%s",out1,out2);
    fclose(html);
    for(j=0;j<N;j++)
    { v[j].clear();
    }
  }
 
  return 0;
}
