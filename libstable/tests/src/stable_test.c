/* tests/stable_test
 * 
 * This program calculates the PDF and CDF of an alpha-stable distribution
 * whith given parameters. It also generates a random sample of desired
 * size.
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
 * along with this program; If not, see <http://www.gnu.org/licenses/ > .
 *
 *  Javier Royuela del Val.
 *  E.T.S.I. Telecomunicación
 *  Universidad de Valladolid
 *  Paseo de Belén 15, 47002 Valladolid, Spain.
 *  jroyval@lpi.tel.uva.es    
 */

#include "stable.h"
#include "methods.h"

#include <stdio.h> 
#include <string.h> 
#include <stdlib.h> 
#include <sys/time.h> 

int print_arch (char name[],int D, int F, int C);

int main (int argc, char *argv[])
{
  char *aux;
  double alpha, beta, sigma, mu, param, xmin, xmax, step, abstol, reltol;
  double *x, *pdf, *cdf, *y, *errpdf, *errcdf;
  StableDist *dist = NULL;
  int thrds, npoints;
  int i=1,F,C;
  int NR=1000;
  struct timeval t_1, t_2;
  double t;
  int method1,method2;
  char methodname[128];

  FILE * f;
  FILE * f2;
  FILE * f3;

  char name[25]  = "./data_stable_pdf.txt";
  char name2[25] = "./data_stable_cdf.txt";
  char name3[25] = "./data_stable_q.txt";

  if (argc==1 || strcmp(argv[1],"-h")==0) {
    printf("Libstable. Copyright (C) 2013  Javier Royuela and Federico Simmross.\n");
    printf("This program comes with ABSOLUTELY NO WARRANTY.\n");
    printf("This is free software, and you are welcome to redistribute it\n");
    printf("under GNU GPLv3 terms and conditions.\n\n");

    printf("Usage: stable_test alpha beta sigma mu param xmin xmax step...\n");
    printf("                   nrandom threads reltol F C\n");
    return 0;
  }

  if (argc  >  1) {  alpha = strtod(argv[i],&aux);      argc--; i++; } else alpha=1.5;
  if (argc  >  1) {   beta = strtod(argv[i],&aux);      argc--; i++; } else beta=0.0;
  if (argc  >  1) {  sigma = strtod(argv[i],&aux);      argc--; i++; } else sigma=1.0;
  if (argc  >  1) {     mu = strtod(argv[i],&aux);      argc--; i++; } else mu=0.0;
  if (argc  >  1) {  param = (int)strtod(argv[i],&aux); argc--; i++; } else param=0;
  if (argc  >  1) {   xmin = strtod(argv[i],&aux);      argc--; i++; } else xmin=-3.0;
  if (argc  >  1) {   xmax = strtod(argv[i],&aux);      argc--; i++; } else xmax=3.0;
  if (argc  >  1) {   step = strtod(argv[i],&aux);      argc--; i++; } else step=0.01;
  if (argc  >  1) {     NR = (int)strtod(argv[i],&aux); argc--; i++; } else NR=1000;
  if (argc  >  1) {  thrds = (int)strtod(argv[i],&aux); argc--; i++; } else thrds=0;
  if (argc  >  1) { reltol = strtod(argv[i],&aux); argc--; i++; } else reltol=1.2e-14;
  if (argc  >  1) {      F = (int)strtod(argv[i],&aux); argc--; i++; } else F=15;
  if (argc  >  1) {      C = (int)strtod(argv[i],&aux); argc--; i++; } else C=70;

  /* Create distribution */
  if((dist = stable_create(alpha,beta,sigma,mu,param)) == NULL) {
        printf("Error while creatring ditribution. Please check introduced data");
        exit(1);
    }

  stable_set_THREADS(thrds);
  stable_set_relTOL(reltol);
  
  vector_step(&x, xmin, xmax, step, &npoints);
  if( x==NULL || npoints==0 ) { exit(1); };

  printf("\n [ alpha =% 1.2f\tbeta =% 1.2f\tgamma =% 1.2f\tdelta =% 1.2f\t]\n",
         alpha,beta,sigma,mu);
  printf(" [ xmin =% 1.2f\txmax =% 1.2f\tstep =% 1.2f\tnpoints =% d  ]\n",
         xmin,xmax,step,npoints);
  printf(" [ reltol =% 1.2e\tabstol = % 1.2e\t]\n",
         stable_get_relTOL(),stable_get_absTOL());
  printf(" [threads = %u\t]\n",stable_get_THREADS());

  pdf = (double *)malloc(sizeof(double)*npoints);
  cdf = (double *)malloc(sizeof(double)*npoints);
  errpdf = (double *)malloc(sizeof(double)*npoints);
  errcdf = (double *)malloc(sizeof(double)*npoints);

  gettimeofday(&t_1,NULL);
  stable_pdf(dist,x,npoints,pdf,errpdf);
  gettimeofday(&t_2,NULL);
  t=t_2.tv_sec-t_1.tv_sec+(t_2.tv_usec-t_1.tv_usec)/1000000.0;
  printf(" -  PDF: %u points in %lf seconds, %lf points/sec\n",
         npoints, t, npoints/t);

  gettimeofday(&t_1,NULL);
  stable_cdf(dist,x,npoints,cdf,errcdf);
  gettimeofday(&t_2,NULL);
  t=t_2.tv_sec-t_1.tv_sec+(t_2.tv_usec-t_1.tv_usec)/1000000.0;
  printf(" -  CDF: %u points in %lf seconds, %lf points/sec\n",
         npoints, t, npoints/t);

  f = fopen(name, "wt");
  f2 = fopen(name2, "wt");
  f3 = fopen("./data_stable_rnd.txt","wt");

  for (i=0;i<npoints;i++)
    {
      fprintf( f,"%1.16lf\t%1.16e\t%1.16e\n",x[i],pdf[i],errpdf[i]);
      fprintf(f2,"%1.16lf\t%1.16e\t%1.16e\n",x[i],cdf[i],errcdf[i]);
    }

  //Generate NR random samples.
  y=(double*)malloc(NR*sizeof(double));
  gettimeofday(&t_1,NULL);
  stable_rnd(dist,y,NR);
  gettimeofday(&t_2,NULL);
  t=t_2.tv_sec-t_1.tv_sec+(t_2.tv_usec-t_1.tv_usec)/1000000.0;
  printf(" - RAND: %u samples generated in %lf seconds, %lf samp/sec\n\n",
         NR, t, NR/t);
  for(i=0;i<NR;i++)
    {
      fprintf(f3,"%1.16e\n",y[i]);
    }

  // Inverse cdf
  stable_set_INV_MAXITER(0);
  
  //Primero la mediana
  double x50 = stable_q_point(dist,0.5,NULL);
  printf("Mediana: x50 = %e\n",x50);

  //Y un barrido en quantiles
  int nq = 99;
  double * q=(double*)malloc(nq*sizeof(double));
  int kq=0;
  for (kq=0;kq<nq;kq++) {
     q[kq] = (kq+1.0)/(nq+1.0);  
  }
  double * inv = (double*)malloc(sizeof(double)*nq);
  gettimeofday(&t_1,NULL);
  stable_q(dist,q,nq,inv,NULL);
  gettimeofday(&t_2,NULL);
  t=t_2.tv_sec-t_1.tv_sec+(t_2.tv_usec-t_1.tv_usec)/1000000.0;
  printf(" - INV: %u quantiles %lf seconds, %lf quant/sec\n\n",
         nq, t, nq/t);
  FILE * f4 = fopen(name3,"wt");
  for (i=0;i<nq;i++) {
    fprintf( f4,"%1.16lf\t%1.16e\t0.0e+00\n",q[i],inv[i]);
  }
  
  // Generated random sample parameter estimation
  // dist parameters are modified by the esetimator.
  stable_fit_koutrouvelis(dist,y,NR);
  printf ("Estimated parameter: %f %f %f %f\n",dist-> alpha,dist-> beta,dist-> sigma,dist-> mu_0);
   
  fclose(f);
  fclose(f2);
  fclose(f3);
  fclose(f4);
  
  i=print_arch(name,2,F,C);
  i=print_arch(name2,2,F,C);
  i=print_arch(name3,2,F,C);

  stable_free(dist);
  free(pdf); free(errpdf);
  free(cdf); free(errcdf);
  free(x);
  free(y);
  free(inv);
  free(q);
  
  return 0;
}

int print_arch (char name[],int D, int F, int C) {

  double CperV, max = -1e300, min=1e300;
  double *valor = NULL, *x = NULL;
  int kmin, kmax, prev_y,N, j, k, nread;
  double *y;
  FILE *file;
  char c_o,c_m;
  char buf[128];

  c_o='.';
  c_m='#';
  
  if (C <= 0) C = 80;
  if (F <= 0) F = 20;
  
  file = fopen(name,"rt");
    
  N = 0;  
  while(!feof(file)) {
    valor = (double *)realloc((double *)valor, (N+1)*sizeof(double));
    x     = (double *)realloc((double *)x, (N+1)*sizeof(double));
    nread = fscanf(file, "%lf\t", &x[N]);
    nread = fscanf(file, "%lf\t", &valor[N]);
    if (fgets(buf, sizeof(buf), file) == NULL) break;
    N++;
  }

  CperV = N / (double)C;
  if (CperV < 1) {
    CperV = 1;
    C = N;
  }

  y = (double*)calloc(C,sizeof(double));
  
  for (j = 0; j < C; j++) {
    kmin = (int)(j * CperV);
    if (kmin > N-1) kmin = N - 1;
    kmax = (int)((j + 1) * CperV);
    if (kmax > N) kmax = N;
    
    for (k = kmin;k < kmax;k++) {
      y[j] += valor[k];
    }
    y[j] = y[j] / (kmax - kmin);
    if (y[j] < min) min = y[j];
    if (y[j] > max) max = y[j];
  }
  for (k = 0; k < C; k++) {
    y[k]  = F*(1.0 - (y[k] - min)/(max - min));
    y[k] -= fmod(y[k], 1.0);
    if (y[k] == F) y[k]--; 
  }
  
//  printf("-----------------------------\n");
//  printf("N=%i C=%i min=%f max=%f CperV=%f\n",N,C,min,max,CperV);
//  printf("-----------------------------\n");
  prev_y=0;
  for (j=0;j<F;j++) {
    printf("% 1.2e ",(double)(F-1-j)/(F-1)*(max-min)+min);
    for (k=0;k<C;k++) {
      if(y[k]==j && prev_y==0) {
        printf("%c",c_m);
        prev_y=1;
      }
      else if(y[k]!=j && prev_y==0) {
        printf("%c",c_o);
        prev_y=1;
      }
      else if(prev_y==1 && y[k]==j) {
        printf("\b*");
        prev_y=1;
      }
      prev_y=0;
    }
    printf("\n");
  }
  if (x[0] > 0.0) printf(" ");
  printf("    %1.3lf",x[0]);
  for (j=0;j<C-11;j++) printf(" ");
  if (x[N-1] > 0.0) printf(" ");
  printf("%1.3lf\n",x[N-1]);
  free(valor);
  free(y);
  fclose(file);
  return 0;
}
