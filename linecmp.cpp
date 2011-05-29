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
{ FILE *fiesire=fopen("iesire.txt","r");
  FILE *fmath=fopen("math.txt","r");
  FILE *html=fopen("html.html","w");
  int i,j,k,l1,l2,max;
  vector<pair<int,int> >v[N];
  pair<int,int> p;
  vector<pair<int,int> >r; 
   
  for (int i=0;i<6;i++)
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
    { for (k=0;k<v[j].size();j++)
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
    r.clear();
    for(j=0;j<N;j++)
    { v[j].clear();
    }
  } 
  return 0;
}
