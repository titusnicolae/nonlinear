#include <stdio.h>
#include <math.h>
float f1(float a,float b,float g,float x,float y,float z)
{ float v[300]; 
  
  v[0]=-475.0;
  v[1]=-464.0;
  v[2]=a;
  v[3]=sin(v[2]);
  v[4]=g;
  v[5]=sin(v[4]);
  v[6]=v[3]*v[5];
  v[7]=cos(v[2]);
  v[8]=0;
  v[9]=b;
  v[10]=sin(v[9]);
  v[11]=v[8]-v[10];
  v[12]=cos(v[4]);
  v[13]=v[11]*v[12];
  v[14]=v[7]*v[13];
  v[15]=v[6]+v[14];
  v[16]=v[1]*v[15];
  v[17]=-260.0;
  v[18]=v[3]*v[12];
  v[19]=v[8]-v[5];
  v[20]=v[11]*v[19];
  v[21]=v[7]*v[20];
  v[22]=v[18]+v[21];
  v[23]=v[17]*v[22];
  v[24]=v[16]+v[23];
  v[25]=2353.0;
  v[26]=cos(v[9]);
  v[27]=v[7]*v[26];
  v[28]=v[25]*v[27];
  v[29]=v[24]+v[28];
  v[30]=v[0]*v[29];
  v[31]=v[7]*v[5];
  v[32]=v[8]-v[3];
  v[33]=v[32]*v[13];
  v[34]=v[31]+v[33];
  v[35]=v[1]*v[34];
  v[36]=v[7]*v[12];
  v[37]=v[32]*v[20];
  v[38]=v[36]+v[37];
  v[39]=v[17]*v[38];
  v[40]=v[35]+v[39];
  v[41]=v[32]*v[26];
  v[42]=v[25]*v[41];
  v[43]=v[40]+v[42];
  v[44]=v[25]*v[43];
  v[45]=v[30]-v[44];
  v[46]=x;
  v[47]=v[45]*v[46];
  v[48]=v[26]*v[12];
  v[49]=v[1]*v[48];
  v[50]=v[26]*v[19];
  v[51]=v[17]*v[50];
  v[52]=v[49]+v[51];
  v[53]=v[25]*v[10];
  v[54]=v[52]+v[53];
  v[55]=v[25]*v[54];
  v[56]=-250.0;
  v[57]=v[56]*v[29];
  v[58]=v[55]-v[57];
  v[59]=y;
  v[60]=v[58]*v[59];
  v[61]=v[47]+v[60];
  v[62]=v[56]*v[43];
  v[63]=v[0]*v[54];
  v[64]=v[62]-v[63];
  v[65]=z;
  v[66]=v[64]*v[65];
  v[67]=v[61]+v[66];
  v[68]=2;
  v[69]=pow(v[67],v[68]);
  v[70]=pow(v[45],v[68]);
  v[71]=pow(v[58],v[68]);
  v[72]=v[70]+v[71];
  v[73]=pow(v[64],v[68]);
  v[74]=v[72]+v[73];
  v[75]=v[69]/v[74];
  v[76]=-760.0;
  v[77]=-271.0;
  v[78]=v[77]*v[15];
  v[79]=-525.0;
  v[80]=v[79]*v[22];
  v[81]=v[78]+v[80];
  v[82]=v[81]+v[28];
  v[83]=v[76]*v[82];
  v[84]=v[77]*v[34];
  v[85]=v[79]*v[38];
  v[86]=v[84]+v[85];
  v[87]=v[86]+v[42];
  v[88]=v[25]*v[87];
  v[89]=v[83]-v[88];
  v[90]=v[89]*v[46];
  v[91]=v[77]*v[48];
  v[92]=v[79]*v[50];
  v[93]=v[91]+v[92];
  v[94]=v[93]+v[53];
  v[95]=v[25]*v[94];
  v[96]=27.0;
  v[97]=v[96]*v[82];
  v[98]=v[95]-v[97];
  v[99]=v[98]*v[59];
  v[100]=v[90]+v[99];
  v[101]=v[96]*v[87];
  v[102]=v[76]*v[94];
  v[103]=v[101]-v[102];
  v[104]=v[103]*v[65];
  v[105]=v[100]+v[104];
  v[106]=pow(v[105],v[68]);
  v[107]=pow(v[89],v[68]);
  v[108]=pow(v[98],v[68]);
  v[109]=v[107]+v[108];
  v[110]=pow(v[103],v[68]);
  v[111]=v[109]+v[110];
  v[112]=v[106]/v[111];
  v[113]=v[75]+v[112];
  v[114]=-432.0;
  v[115]=-65.0;
  v[116]=v[115]*v[15];
  v[117]=-300.0;
  v[118]=v[117]*v[22];
  v[119]=v[116]+v[118];
  v[120]=v[119]+v[28];
  v[121]=v[114]*v[120];
  v[122]=v[115]*v[34];
  v[123]=v[117]*v[38];
  v[124]=v[122]+v[123];
  v[125]=v[124]+v[42];
  v[126]=v[25]*v[125];
  v[127]=v[121]-v[126];
  v[128]=v[127]*v[46];
  v[129]=v[115]*v[48];
  v[130]=v[117]*v[50];
  v[131]=v[129]+v[130];
  v[132]=v[131]+v[53];
  v[133]=v[25]*v[132];
  v[134]=297.0;
  v[135]=v[134]*v[120];
  v[136]=v[133]-v[135];
  v[137]=v[136]*v[59];
  v[138]=v[128]+v[137];
  v[139]=v[134]*v[125];
  v[140]=v[114]*v[132];
  v[141]=v[139]-v[140];
  v[142]=v[141]*v[65];
  v[143]=v[138]+v[142];
  v[144]=pow(v[143],v[68]);
  v[145]=pow(v[127],v[68]);
  v[146]=pow(v[136],v[68]);
  v[147]=v[145]+v[146];
  v[148]=pow(v[141],v[68]);
  v[149]=v[147]+v[148];
  v[150]=v[144]/v[149];
  v[151]=v[113]+v[150];
  v[152]=585.0;
  v[153]=191.0;
  v[154]=v[153]*v[15];
  v[155]=645.0;
  v[156]=v[155]*v[22];
  v[157]=v[154]+v[156];
  v[158]=v[157]+v[28];
  v[159]=v[152]*v[158];
  v[160]=v[153]*v[34];
  v[161]=v[155]*v[38];
  v[162]=v[160]+v[161];
  v[163]=v[162]+v[42];
  v[164]=v[25]*v[163];
  v[165]=v[159]-v[164];
  v[166]=v[165]*v[46];
  v[167]=v[153]*v[48];
  v[168]=v[155]*v[50];
  v[169]=v[167]+v[168];
  v[170]=v[169]+v[53];
  v[171]=v[25]*v[170];
  v[172]=606.0;
  v[173]=v[172]*v[158];
  v[174]=v[171]-v[173];
  v[175]=v[174]*v[59];
  v[176]=v[166]+v[175];
  v[177]=v[172]*v[163];
  v[178]=v[152]*v[170];
  v[179]=v[177]-v[178];
  v[180]=v[179]*v[65];
  v[181]=v[176]+v[180];
  v[182]=pow(v[181],v[68]);
  v[183]=pow(v[165],v[68]);
  v[184]=pow(v[174],v[68]);
  v[185]=v[183]+v[184];
  v[186]=pow(v[179],v[68]);
  v[187]=v[185]+v[186];
  v[188]=v[182]/v[187];
  v[189]=v[151]+v[188];
  v[190]=586.0;
  v[191]=-89.0;
  v[192]=v[191]*v[15];
  v[193]=593.0;
  v[194]=v[193]*v[22];
  v[195]=v[192]+v[194];
  v[196]=v[195]+v[28];
  v[197]=v[190]*v[196];
  v[198]=v[191]*v[34];
  v[199]=v[193]*v[38];
  v[200]=v[198]+v[199];
  v[201]=v[200]+v[42];
  v[202]=v[25]*v[201];
  v[203]=v[197]-v[202];
  v[204]=v[203]*v[46];
  v[205]=v[191]*v[48];
  v[206]=v[193]*v[50];
  v[207]=v[205]+v[206];
  v[208]=v[207]+v[53];
  v[209]=v[25]*v[208];
  v[210]=316.0;
  v[211]=v[210]*v[196];
  v[212]=v[209]-v[211];
  v[213]=v[212]*v[59];
  v[214]=v[204]+v[213];
  v[215]=v[210]*v[201];
  v[216]=v[190]*v[208];
  v[217]=v[215]-v[216];
  v[218]=v[217]*v[65];
  v[219]=v[214]+v[218];
  v[220]=pow(v[219],v[68]);
  v[221]=pow(v[203],v[68]);
  v[222]=pow(v[212],v[68]);
  v[223]=v[221]+v[222];
  v[224]=pow(v[217],v[68]);
  v[225]=v[223]+v[224];
  v[226]=v[220]/v[225];
  v[227]=v[189]+v[226];
  v[228]=160.0;
  v[229]=-462.0;
  v[230]=v[229]*v[15];
  v[231]=208.0;
  v[232]=v[231]*v[22];
  v[233]=v[230]+v[232];
  v[234]=v[233]+v[28];
  v[235]=v[228]*v[234];
  v[236]=v[229]*v[34];
  v[237]=v[231]*v[38];
  v[238]=v[236]+v[237];
  v[239]=v[238]+v[42];
  v[240]=v[25]*v[239];
  v[241]=v[235]-v[240];
  v[242]=v[241]*v[46];
  v[243]=v[229]*v[48];
  v[244]=v[231]*v[50];
  v[245]=v[243]+v[244];
  v[246]=v[245]+v[53];
  v[247]=v[25]*v[246];
  v[248]=-214.0;
  v[249]=v[248]*v[234];
  v[250]=v[247]-v[249];
  v[251]=v[250]*v[59];
  v[252]=v[242]+v[251];
  v[253]=v[248]*v[239];
  v[254]=v[228]*v[246];
  v[255]=v[253]-v[254];
  v[256]=v[255]*v[65];
  v[257]=v[252]+v[256];
  v[258]=pow(v[257],v[68]);
  v[259]=pow(v[241],v[68]);
  v[260]=pow(v[250],v[68]);
  v[261]=v[259]+v[260];
  v[262]=pow(v[255],v[68]);
  v[263]=v[261]+v[262];
  v[264]=v[258]/v[263];
  v[265]=v[227]+v[264]; 
  return v[265];
}

int main ()
{ 
  float x=10000.0;
  float y=-305.0377;
  float z=2590.8471;
  float a=0.010202;
  float b=-0.834814;
  float g=0.042359;
  int i=0;
  for(i=0;i<1000000;i++)
  { f1(a,b,g,x,y,z);
  }

  printf("%f",f1(a,b,g,x,y,z));
  return 0;
}
