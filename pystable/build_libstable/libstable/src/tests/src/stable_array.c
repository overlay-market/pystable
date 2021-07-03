/** @file stable_array.c
 * 
 * This program generates an array complete set of PDF or CDF evaluations
 * of standard alpha-stable distributions on a regular sweep of the
 * alpha-beta parameter space.
 * THIS PROGRAM OBTATINS A LARGE SET OF DATA POINTS. ITS INTENDED FOT
 * LIBSTABLE EVALUATION PURPOSES
 *
 *
 * Copyright (C) 2013. Javier Royuela del Val
 *                     Federico Simmross Wattenberg
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 3 of the License.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; If not, see <http://www.gnu.org/licenses/>.
 *
 *
 *  Javier Royuela del Val.
 *  E.T.S.I. Telecomunicación
 *  Universidad de Valladolid
 *  Paseo de Belén 15, 47002 Valladolid, Spain.
 *  jroyval@lpi.tel.uva.es    
 */

#include "stable.h"

#include "methods.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

int main (int argc, char *argv[])
{
  double alpha0,alphaN,alphaD,beta0,betaN,betaD,x0,xN,xD,gamma,delta,tol,atol;
  double *pdf,*alpha,*beta,*x,*err;

  StableDist *dist = NULL;
  int i=1,j,k;
  int Na,Nb,Nx;
  int n,P,aux;
  void(*func)(StableDist *, const double *, const unsigned int,
              double *, double *);

  struct timeval t_1,t_2,tp_1,tp_2;
  double t,tpdf;

  char name[256],nameerr[256],nametiempos[256];
  FILE * f;
  FILE * ferr;
  FILE * ftiempos;
  
  printf("\n");
  printf("  A the pdf or the cdf will be evaluated for a set of parameters. Enter choice:.\n");
  printf("    1 for pdf calculations\n");
  printf("    2 for cdf calculations\n");
  printf("  Enter choice: ");
  aux=scanf("%d",&n);

  printf("  Enter parametrization: ");
  aux=scanf("%d",&P);
  printf("  First alpha, last alpha and alpha stepsize: ");
  aux=scanf("%lf %lf %lf",&alpha0,&alphaN,&alphaD);
  printf("  First beta, last beta and beta stepsize: ");
  aux=scanf("%lf %lf %lf",&beta0,&betaN,&betaD);
  printf("  First x, last x and x stepsize: ");
  aux=scanf("%lf %lf %lf",&x0,&xN,&xD);
  printf("  Gamma and Delta: ");
  aux=scanf("%lf %lf",&gamma,&delta);
  printf("  Absolute Tolerance to Error: ");
  aux=scanf("%lf",&atol);
  printf("  Relative Tolerance to Error: ");
  aux=scanf("%lf",&tol);

  /* Parameters and x points*/
  vector_step(&alpha, alpha0, alphaN, alphaD, &Na);
  vector_step(&beta, beta0, betaN, betaD, &Nb);
  vector_step(&x, x0, xN, xD, &Nx);
  pdf = (double*)malloc(Nx*Nb*sizeof(double));
  err = (double*)malloc(Nx*Nb*sizeof(double));

  #ifdef DEBUG
    printf("\n");
    printf(" % 10.5lf:% 10.5lf:% 10.5lf",alpha[0],alphaD,alpha[Na-1]);
    printf("\n");
    printf(" % 10.5lf:% 10.5lf:% 10.5lf",beta[0],betaD,beta[Nb-1]);
    printf("\n");
    printf(" % 10.5lf:% 10.5lf:% 10.5lf",x[0],xD,x[Nx-1]);
    printf("\n");
  #endif
   
  if (n==1)
    {
      func = &stable_pdf;
      strcpy(name,"data_stable_array_pdf.txt");
      strcpy(nameerr,"data_stable_array_pdf_err.txt");
      strcpy(nametiempos,"data_stable_array_pdf_times.txt");
    }
  else if (n==2)
    {
      func = &stable_cdf;
      strcpy(name,"data_stable_array_cdf.txt");
      strcpy(nameerr,"data_stable_array_cdf_err.txt");
      strcpy(nametiempos,"data_stable_array_pdf_times.txt");
    }
  else { printf("ERROR"); exit (2);}

  if((f=fopen(name, "wt"))==NULL)
    {
      printf("Open file error.");
      exit(2);
    }

  if((ferr=fopen(nameerr, "wt"))==NULL)
    {
      printf("Open file error.");
      exit(2);
    }

  if((ftiempos=fopen(nametiempos, "wt"))==NULL)
    {
      printf("Open file error.");
      exit(2);
    }

  /* Create distribution */
  if((dist = stable_create(alpha[0],beta[0],gamma,delta,P)) == NULL)
    {
      printf("Distribution creation error");
      exit(EXIT_FAILURE);
    }

  stable_set_THREADS(0);
  stable_set_relTOL(tol);
  stable_set_absTOL(atol);
  printf("FUNCTION=%d ALPHAPOINTS=%d BETAPOINTS=%d XPOINTS=%d\n",n,Na,Nb,Nx);
  
  fprintf(f,"FUNCTION=%d ALPHAPOINTS=%d BETAPOINTS=%d XPOINTS=%d\n",n,Na,Nb,Nx);
  fprintf(ferr,"FUNCTION=%d ALPHAPOINTS=%d BETAPOINTS=%d XPOINTS=%d\n",n,Na,Nb,Nx);
  tpdf=0;
  gettimeofday(&t_1,NULL);
  for(j=0;j<Na;j++)
    {
      for(i=0;i<Nb;i++)
        {
          stable_setparams(dist,alpha[j],beta[i],gamma,delta,P);
          gettimeofday(&tp_1,NULL);
          (func)(dist,(const double *)x,Nx,pdf+i*Nx,err+i*Nx);
          printf("        -> Alpha = %lf, Beta = %lf, %d points OK <-\n",
                 alpha[j],beta[i],Nx);
          gettimeofday(&tp_2,NULL);
          tpdf=tp_2.tv_sec-tp_1.tv_sec+(tp_2.tv_usec-tp_1.tv_usec)/1000000.0;
          fprintf(ftiempos,"%lf %lf %lf",alpha[j],beta[i],tpdf);
        }

      // Dump data to text file 
      fprintf(f,"\nAlpha = %lf\n________x\\beta________\t",alpha[j]);      
      fprintf(ferr,"\nAlpha = %lf\n________x\\beta________\t",alpha[j]);
      fprintf(f,"%lf\t",alpha[j]);      
      fprintf(ferr,"%lf\t",alpha[j]);
      for(i=0;i<Nb;i++)
        {
          fprintf(f,"%1.16e\t",beta[i]);
          fprintf(ferr,"%1.16e\t",beta[i]);
        }
      fprintf(f,"\n");
      fprintf(ferr,"\n");
      for(k=0;k<Nx;k++)
        {
          fprintf(f,"%1.16e\t",x[k]);
          fprintf(ferr,"%1.16e\t",x[k]);
          for(i=0;i<Nb;i++)
            {
              fprintf(f,"%1.16e\t",*(pdf+i*Nx+k));
              fprintf(ferr,"%1.16e\t",*(err+i*Nx+k));
            }
          fprintf(f,"\n");
          fprintf(ferr,"\n");
        }
      
    }
  gettimeofday(&t_2,NULL);
  t=t_2.tv_sec-t_1.tv_sec+(t_2.tv_usec-t_1.tv_usec)/1000000.0;

  printf("\n-----> Computations done in %3.3lf seconds <-----\n",t);

  fclose(f);
  fclose(ferr);
  fclose(ftiempos);

    return 0;
}
