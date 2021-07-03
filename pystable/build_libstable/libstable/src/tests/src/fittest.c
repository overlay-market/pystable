/* tests/fittest
 *
 * Example program that test Libstable parameter estimation methods.
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
#include <time.h>
#include <stdlib.h>

int main (int argc, char* argv[])
{
  char *aux;
  double alpha, beta, sigma, mu;
  double ma=0,mb=0,ms=0,mm=0,va=0,vb=0,vs=0,vm=0;
  double * data;
  int i=1,iexp,N,Nexp;
  int seed;

  StableDist *dist = NULL;

  if (argc>1) {  alpha = strtod(argv[i],&aux); argc--; i++; } else alpha=1.5;
  if (argc>1) {  beta = strtod(argv[i],&aux); argc--; i++; } else beta=0.75;
  if (argc>1) { sigma = strtod(argv[i],&aux); argc--; i++; } else sigma=5.0;
  if (argc>1) {    mu = strtod(argv[i],&aux); argc--; i++; } else mu=15.0;
  if (argc>1) {     N = (int)strtod(argv[i],&aux); argc--; i++; } else N=100;
  if (argc>1) {  Nexp = (int)strtod(argv[i],&aux); argc--; i++; } else Nexp=100;
  if (argc>1) {  seed = (int)strtod(argv[i],&aux); argc--; i++; } else seed=-1;

  printf("%f %f %f %f %d %d\n",alpha,beta,sigma,mu,N,Nexp);
  if ((dist = stable_create(alpha,beta,sigma,mu,0)) == NULL) {
        printf("Error when creating the distribution");
        exit(1);
    }

  stable_set_THREADS(1);
  stable_set_absTOL(1e-16);
  stable_set_relTOL(1e-8);

  if (seed<0) stable_rnd_seed(dist,time(NULL));
  else stable_rnd_seed(dist,seed);

  /* Random sample generation */
  data = (double*)malloc(N*Nexp*sizeof(double));

  stable_rnd(dist,data,N*Nexp);

  for(iexp=0;iexp<Nexp;iexp++)
   {
     printf("o");fflush(stdout);

     stable_fit_init(dist,data+iexp*N,N,NULL,NULL);

      /* Select estimation algorithm to test */
     stable_fit_mle(dist,data+iexp*N,N);
     //stable_fit_mle2d(dist,data+iexp*N,N);
     //stable_fit_koutrouvelis(dist,data+iexp*N,N);

     ma+=dist->alpha;
     mb+=dist->beta;
     ms+=dist->sigma;
     mm+=dist->mu_0;

     va+=dist->alpha*dist->alpha;
     vb+=dist->beta*dist->beta;
     vs+=dist->sigma*dist->sigma;
     vm+=dist->mu_0*dist->mu_0;

     printf("\b.");
     fflush(stdout);
   }
  printf(" DONE\n");
  ma=ma/Nexp;
  va=sqrt((va/Nexp-ma*ma)*Nexp/(Nexp-1));
  mb=mb/Nexp;
  vb=sqrt((vb/Nexp-mb*mb)*Nexp/(Nexp-1));
  ms=ms/Nexp;
  vs=sqrt((vs/Nexp-ms*ms)*Nexp/(Nexp-1));
  mm=mm/Nexp;
  vm=sqrt((vm/Nexp-mm*mm)*Nexp/(Nexp-1));

  printf("-----------------------------------------------------------\n");
  printf("Alpha = %f+-%f\n",ma,va);
  printf("Beta  = %f+-%f\n",mb,vb);
  printf("Sigma = %f+-%f\n",ms,vs);
  printf("Mu    = %f+-%f\n",mm,vm);

  free(data);
  stable_free(dist);

  fclose(stable_get_FLOG());

  return 0;
}
