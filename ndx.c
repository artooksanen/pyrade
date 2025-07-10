#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <stdint.h>

char *strupr(char *str)
{
  unsigned char *p = (unsigned char *)str;

  while (*p) {
     *p = toupper((unsigned char)*p);
      p++;
  }

  return str;
}


FILE *ndxfile;

#pragma pack(push)  /* push current alignment to stack */
#pragma pack(1)     /* set alignment to 1-byte boundary */

struct NDXREC
   {
   char string[10];
//   long ra,de,ptr;
   int ra,de;
   int ptr;
   };

#pragma pack(pop)   /* restore original alignment from stack */

int openndx(lastrec)
unsigned int lastrec;
{
   int sta=1;
   ndxfile=fopen("index.sor","r+b");
   if(ndxfile==NULL) printf("** tiedoston INDEX.SOR avausvirhe\n");
/*
   if(ndxfile!=NULL) sta=readndx(0,name,&lastrec);
*/
   return(sta);
}

int closendx()
{
   return(fclose(ndxfile));
}

int readndx(row,name,ra,de,ptr)
unsigned int row;                  /* row to read   */
char *name;
float *ra,*de;
long *ptr;
{
      struct NDXREC data;
      long offset;
      int sta,k;
//      printf("size of struct NDXREC:%ld\n",sizeof(struct NDXREC));
      offset=(long) sizeof(struct NDXREC)*row;
      sta=fseek(ndxfile,offset,SEEK_SET);
      if(sta==0)
      fread(&data,sizeof(struct NDXREC),1,ndxfile);
//      printf("readndx:row=%d data.string=%s\n",row,data.string);
//      printf("readndx:data.ra=%d %f\n",data.ra,data.ra/3600.0);
//      printf("readndx:data.de=%d %f\n",data.de,data.de/60.0);
      *ra=data.ra/3600.0; 
      *de=data.de/60.0; 
      *ptr=data.ptr; 
      for(k=0;k<10;k++) name[k]=data.string[k];
      name[10]=0;
      return(sta);
}


int writendx(row,name,ra,de,ptr)
unsigned int row;                  /* row to read   */
char *name;
double ra,de;
long ptr;
{
      struct NDXREC data;  
      long offset;
      int sta,j;
      offset=(long) sizeof(struct NDXREC)*row;
      sta=fseek(ndxfile,offset,SEEK_SET);
      if(sta==0)
      for(j=0;j<10;j++) data.string[j]=name[j];
      data.ra=ra*3600;
      data.de=de*60;
      data.ptr=ptr;
      fwrite(&data,sizeof(struct NDXREC),1,ndxfile);
      return(sta);
}

int searchndx(nimi)
char *nimi;
{
   char text[10];
   int i,j,a,c,b,k,l;
   unsigned int last;
   float ra,de;
   long ptr;

   strupr(nimi);
   printf("Searching...\n"); 
   a=-1;
   b=15984;
   l=-1;
   loop:
   c=(a+b)/2;
   readndx(c,text,&ra,&de,&ptr);
   printf("tietue %4.4d: %s\n",c,text);
    for(k=0;k<10;k++)
     {
     if(text[k]<nimi[k]) {a=c;break;}
     if(text[k]>nimi[k]) {b=c;break;}
     if((text[k]==0)&(nimi[k]==0)) {l=c;a=c;b=c;break;}
     if(k==9) {l=c;a=c;b=c;break;}
     if(nimi[k]==0) {b=c;break;}
     }
   if(((c==a)|(c==b))&((b-a)>1)) goto loop;
   
      if(l>-1) printf("tietue %4.4d: %-10s ra:%5f de:%5f ptr:%6ld\n",c,text,ra,de,ptr); 
      else printf("ei löytynyt: %s\n",nimi); 
   
   return(l);
   }
