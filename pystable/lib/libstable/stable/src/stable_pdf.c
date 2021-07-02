/* stable/stable_pdf.c
 * 
 * Code for computing the PDF of an alpha-estable distribution.
 * Expresions presented in [1] are employed.
 *
 * [1] Nolan, J. P. Numerical Calculation of Stable Densities and
 *     Distribution Functions Stochastic Models, 1997, 13, 759-774
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
#include "stable_integration.h"

#include "methods.h"
#include <pthread.h>

double stable_pdf_g1(double theta, void *args)
{
  StableDist *dist = (StableDist *)args;
  double g, V, aux;

//  g   = dist->beta_;
//  aux = theta+dist->theta0_;
//  V   = M_PI_2-theta;

//  if ((g==1 && aux < THETA_TH*1.1) || (g==-1 && V<THETA_TH*1.1)) {
//    V = dist->Vbeta1;// printf("");
//  }
//  else {
    aux = (dist->beta_*theta+M_PI_2)/cos(theta);
    V = sin(theta)*aux/dist->beta_ + log(aux) + dist->k1;
//  }
  #ifdef DEBUG
  integ_eval++;
  #endif

  g = V + dist->xxipow;
  //Obtenemos log(g), en realidad
  //Taylor: exp(-x) ~ 1-x en x ~ 0 
  //Si g<1.52e-8 -> exp(-g)=(1-g) -> g·exp(-g) = g·(1-g) con precision double.
  //Asi nos ahorramos calcular una exponencial. (que es costoso).
  if (isnan(g)) return 0.0;
  if((g=exp(g)) < 1.522e-8 ) return (1.0-g)*g;
  g = exp(-g)*g;
  if (isnan(g) || g<0) return 0.0;

  /*fprintf(FINTEG,"%1.4f\t%1.4f\t%1.6f\t%1.6e\n",
          dist->alpha,dist->beta_,theta,g);*/

//  else return g;
  return g;
}

double stable_pdf_g2(double theta, void *args)
{
  StableDist *dist = (StableDist *)args;
  double g, cos_theta,aux,V;

//  g   = dist->beta_;
//  aux = theta+dist->theta0_;
//  V   = M_PI_2-theta;

//  if ((g==1 && aux < THETA_TH*1.1 && dist->alpha <1) || (g==-1 && V<THETA_TH*1.1 && dist->alpha>1)) {
//    V = dist->Vbeta1;// printf("");
 // }
//  else {

  cos_theta = cos(theta);
  aux = (dist->theta0_+theta)*dist->alpha;
  V = log(cos_theta/sin(aux))*dist->alphainvalpha1 +
       + log(cos(aux-theta)/cos_theta) + dist->k1;
//  }

  #ifdef DEBUG
  integ_eval++;
  #endif

  g = V + dist->xxipow;
  //g>6.55 -> exp(g-exp(g)) < 2.1E-301
  if(g>6.55 || g<-700) return 0.0;
  //Taylor: x·exp(-x) ~ x·(1-x) cuando x ~ 0 
  //Si g < 1.52e-8 -> g·exp(-g) = g·(1-g) con precision double.
  //Asi nos ahorramos calcular una exponencial (que es costoso).
  else  g=exp(g);
//  if(isnan(g) || isinf(g)) {return 0.0;}
//  else if (g < 1.522e-8) {return (1.0-g)*g;}
/*  else*/ g = exp(-g)*g;
  if (isnan(g) || isinf(g) || g<0) {return 0.0;}
/* 
  fprintf(FINTEG,"%1.16lf\t%1.16lf\t%1.16lf\t%1.16e\n",
          dist->alpha,dist->beta_,theta,g);
*/

  return g;
}

double stable_pdf_g(double theta, void *args)
{
  StableDist * dist = (StableDist *)args;
  if (dist->ZONE == ALPHA_1) {
    return stable_pdf_g1(theta, args); }
  else if (dist->ZONE == CAUCHY) {
    return -1.0; }
  else {
    return stable_pdf_g2(theta, args); }
}

double stable_g_aux1(double theta, void *args)
{
  StableDist *dist = (StableDist *)args;
  double g, V,aux;

  aux = (dist->beta_*theta+M_PI_2)/cos(theta);
  V = sin(theta)*aux/dist->beta_ + log(aux) + dist->k1;
  g = V + dist->xxipow;

//  printf("%lf %lf %lf",theta,V,g); getchar();

  #ifdef DEBUG
  integ_eval++;
  #endif

//  if (isnan(g)) { return -HUGE_VAL; }
//  else return g;
  return g;
}

double stable_g_aux2(double theta, void *args)
{
  StableDist *dist = (StableDist *)args;
  double g, cos_theta,aux,V;

  cos_theta = cos(theta);
  aux = (dist->theta0_+theta)*dist->alpha;
  V = log(cos_theta/sin(aux))*dist->alphainvalpha1 +
       + log(cos(aux-theta)/cos_theta) + dist->k1;

  g = V + dist->xxipow;

  #ifdef DEBUG
  integ_eval++;
  #endif
//  if (g > 1.0) return 1.0;
//  else if(g < 0.0 || isnan(g)) return 0.0;
//  else return g;
  return g;
}

double stable_g_aux(double theta, void *args)
{
  StableDist *dist = (StableDist *)args;

  if (dist->ZONE==ALPHA_1)
    return stable_g_aux1(theta,args);
  else
    return stable_g_aux2(theta,args);
}

void * thread_init_pdf(void *ptr_args)
{
  StableArgsPdf *args = (StableArgsPdf *)ptr_args;
  int counter_ = 0;

  while (counter_ < args->Nx)
    {
      args->pdf[counter_]=(*(args->ptr_funcion))(args->dist,args->x[counter_],
                                                 &(args->err[counter_]));
      counter_++;
    }
  pthread_exit(NULL);
}

void stable_pdf(StableDist *dist, const double* x, const unsigned int Nx,
                double *pdf, double *err)
{
  int Nx_thread[THREADS],
      initpoint[THREADS],
      k,flag=0;
  void *status;
  pthread_t threads[THREADS];
  StableArgsPdf args[THREADS];
  
/* Si no se introduce el puntero para el error, se crea*/
  if (err==NULL) {flag=1;err=(double*)malloc(Nx*sizeof(double));}

/* Reparto de los puntos de evaluacion entre los hilos disponibles */

  Nx_thread[0] = Nx/THREADS;
  if (0 < Nx%THREADS) Nx_thread[0]++;

  initpoint[0] = 0;
  for(k=1;k<THREADS;k++)
    {
      Nx_thread[k] = Nx/THREADS;
      if (k < Nx%THREADS) Nx_thread[k]++;
      initpoint[k] = initpoint[k-1] + Nx_thread[k-1];
    }

/* Creacion de los hilos, pasando a cada uno una copia de la distribucion */

  for(k=0; k<THREADS; k++)
    {
      args[k].ptr_funcion = dist->stable_pdf_point;

      args[k].dist = stable_copy(dist);
      args[k].pdf  = pdf+initpoint[k];
      args[k].x    = x+initpoint[k];
      args[k].Nx   = Nx_thread[k];
      args[k].err  = err+initpoint[k];

      if(pthread_create(&threads[k], NULL, thread_init_pdf, (void *)&args[k]))
        {
          perror("Error en la creacion de hilo");
          if (flag==1) free(err);
          return;
        }
    }

/* Esperar a finalizacion de todos los hilos */
  for(k=0; k<THREADS; k++)
    {
      pthread_join(threads[k], &status);
    }

/* Liberar las copias de la distribucion realizadas */
  for(k=0; k<THREADS; k++)
    {
      stable_free(args[k].dist);
    }
    
  if (flag==1) free(err);
}

/******************************************************************************/
/*   Estrategia de integracion para PDF                                       */
/******************************************************************************/

double
stable_integration_pdf_low(StableDist *dist, double(*integrando)(double,void*),
                  double(*integ_aux)(double,void*), double *err)
/*esta es estrategia de baja precision: 2 intervalos de integracion:simetrico en
torno al maximo y el resto*/
{
  int warnz[5],k;
  double pdf=0,
         pdf_aux=0,pdf1=0,/*pdf2=0.0,pdf3=0.0,*/
         err_aux=0;
  double theta[5];
  //int method_;

  #ifdef DEBUG
  int aux_eval=0;
  #endif

  theta[0] = -dist->theta0_+THETA_TH; warnz[0]=0;
  theta[4] = M_PI_2 - THETA_TH;
  theta[2] = zbrent(integ_aux,(void*)dist,theta[0],theta[4],
                         0.0,1e-6*(theta[4]-theta[0]),&k);

  switch (k)
    {
      case 0:   //Max en el interior del intervalo de integracion.
    // Crea intervalo simetrico entorno al maximo con el punto encontrado
    // mas proximo a el y los otros intervalos:
        if (theta[2]-theta[0] < theta[4]-theta[2]) {
          theta[2]=theta[2]*2.0-theta[0];
        }
        else
         {
           pdf_aux=theta[0];
           theta[0]=theta[4];
           theta[4]=pdf_aux;
           theta[2]=theta[2]*2.0-theta[0];
         }
        break;

      case -2: //Max en el borde izquierdo del intervalo
        // puede pasar si beta=+-1 y alpha<1        //  .
        pdf1=(integrando)(theta[0],(void*)dist);

        theta[2]=zbrent(integrando,(void*)dist,theta[0],theta[4],
                         pdf1*1e-6,1e-6*(theta[4]-theta[0]),&warnz[2]);
        break;

      case  -1: //Max en el borde derecho del intervalo
        // puede pasar si beta=+-1 y alpha<1
        theta[1]=theta[4];
        theta[4]=theta[0];
        theta[0]=theta[1];

        pdf1=(integrando)(theta[0],(void*)dist);

        theta[2]=zbrent(integrando,(void*)dist,theta[4],theta[0],
                         pdf1*1e-6,1e-6*(theta[0]-theta[4]),&warnz[2]);
        break;

      default: // Nunca llegara aqui
        theta[1] = 0.5*(theta[4]-theta[2]);
        theta[3] = 0.5*(theta[2]+theta[0]);
        break;
    }

  #ifdef DEBUG
  aux_eval=integ_eval;
  integ_eval=0;
  #endif

  stable_integration(dist,integrando,theta[0],theta[2],
                             absTOL,relTOL,IT_MAX,
                             &pdf_aux,&err_aux,STABLE_QAG2);
  pdf=fabs(pdf_aux);
  *err=err_aux*err_aux;

  #ifdef DEBUG
  warnz[0]=integ_eval;
  integ_eval=0;
  #endif
/*
  printf("%e %e\n",max(pdf*relTOL,absTOL)*0.5,relTOL);
  getchar();
*/
  stable_integration(dist,integrando,theta[2],theta[4],
                             max(pdf*relTOL,absTOL)*0.5,relTOL,IT_MAX,
                             &pdf_aux,&err_aux,STABLE_QAG2);
  pdf+=fabs(pdf_aux);
  *err+=err_aux*err_aux;
  #ifdef DEBUG
  warnz[1]=integ_eval;
  integ_eval=0;
  #endif

  *err=sqrt(*err)/pdf;

  #ifdef DEBUG
  fprintf(FINTEG,"%+1.3e % 1.3e % 1.3e",x,pdf,*err);
  fprintf(FINTEG," %+1.3e %+1.3e %+1.3e %+1.3e %+1.3e",theta[0],theta[1],theta[2],theta[3],theta[4]);
  fprintf(FINTEG," % 1.3e % 1.3e % 1.3e % 1.3e", pdf1,pdf2,pdf3,fabs(pdf_aux));
  fprintf(FINTEG," %d %d %d %d %d %d\n",
          warnz[0],warnz[1],warnz[2],integ_eval,aux_eval,
          warnz[0]+warnz[1]+warnz[2]+integ_eval+aux_eval);
  printf("abstols % 1.3e % 1.3e % 1.3e % 1.3e \n",absTOL,max(pdf1*relTOL,absTOL)*0.5,max((pdf2+pdf1)*relTOL,absTOL)*0.25,max((pdf3+pdf2+pdf1)*relTOL,absTOL)*0.25);
  #endif

  return pdf;
}

double
stable_integration_pdf(StableDist *dist, double(*integrando)(double,void*),
                  double(*integ_aux)(double,void*), double *err)
{
/* Este caso se da en:
       x >> xi con alpha > 1
       x ~  xi con alpha < 1
       x >> 0  con alpha = 1 y beta < 0
       x << 0  con alpha = 1 y beta > 0 */

/* Estrategia:
     - Busca el máximo del integrando: theta[2]
     - Busca puntos donde integrando cae por debajo de un umbral
     - 1 - Integra en intervalo simetrico entorno al maximo
     - 2 - Integra el resto que queda por encima del umbral
     - 3 y 4 - Integra en los bordes por debajo del umbral
     - Suma todo */

  int warnz[5],k;
  double pdf=0,
         pdf_aux=0,pdf1=0,pdf2=0.0,pdf3=0.0,
         err_aux=0;
  double theta[5];
  //int method_;

  #ifdef DEBUG
  int aux_eval=0;
  #endif

  theta[0] = -dist->theta0_+THETA_TH; warnz[0]=0;
  theta[4] = M_PI_2 - THETA_TH;
  theta[2] = zbrent(integ_aux,(void*)dist,theta[0],theta[4],
                         0.0,1e-9*(theta[4]-theta[0]),&k);

  switch (k)
    {
      case 0:   //Max en el interior del intervalo de integracion.
        // Busca puntos donde integrando cae por debajo de umbral
        pdf1 = (integ_aux)(theta[0],(void*)dist);
        pdf2 = (integ_aux)(theta[4],(void*)dist);

        if (fabs(AUX1)>fabs(pdf1)) {
        //  printf("1 %1.1lf ",x);
          theta[1]=theta[0]+1e-2*(theta[2]-theta[0]);
        }
        else {
          theta[1] = zbrent(integ_aux,(void*)dist,theta[0],theta[2],
                        AUX1, 1e-9*(theta[2]-theta[0]),&warnz[1]);
		}

        if (fabs(AUX2)>fabs(pdf2)) {
        //  printf("2 %1.1lf ",x);
          theta[3]=theta[4]-1e-2*(theta[4]-theta[2]);
        }
        else {
	 	  theta[3] = zbrent(integ_aux,(void*)dist,theta[2],theta[4],
                        AUX2, 1e-9*(theta[4]-theta[2]),&warnz[3]);
        }

    // Crea intervalo simetrico entorno al maximo con el punto encontrado
    // mas proximo a el y los otros intervalos:
        if (theta[2]-theta[1] < theta[3]-theta[2]) {
          theta[2]=theta[2]*2.0-theta[1];
        }
        else
         {
           pdf_aux=theta[0];                 //            .
           theta[0]=theta[4];                //           /|\    .
           theta[4]=pdf_aux;                 //         /  | \   .
           pdf_aux=theta[3];                 //_______/ |  |  \___
           theta[3]=theta[1];                //4      3 2  |   1 0
           theta[1]=pdf_aux;
           theta[2]=theta[2]*2.0-theta[1];
         }
        break;

      case -2: //Max en el borde izquierdo del intervalo
        // puede pasar si beta=+-1 y alpha<1        //  .
        theta[1]=theta[0];
        pdf1=(integrando)(theta[1],(void*)dist);

        theta[2]=zbrent(integrando,(void*)dist,theta[1],theta[4],
                         pdf1*1e-6,1e-9*(theta[4]-theta[1]),&warnz[2]);
        pdf1=stable_pdf_g(theta[2],(void*)dist);
        theta[3]=zbrent(integrando,(void*)dist,theta[2],theta[4],
                         pdf1*1e-6,1e-9*(theta[4]-theta[2]),&warnz[2]);
        pdf1=stable_pdf_g(theta[3],(void*)dist);

        break;

      case  -1: //Max en el borde derecho del intervalo
        // puede pasar si beta=+-1 y alpha<1
        theta[1]=theta[4];
        theta[4]=theta[0];
        pdf1=(integrando)(theta[1],(void*)dist);

        theta[2]=zbrent(integrando,(void*)dist,theta[4],theta[1],
                         pdf1*1e-6,1e-9*(theta[1]-theta[4]),&warnz[2]);
        pdf1=stable_pdf_g(theta[2],(void*)dist);
        theta[3]=zbrent(integrando,(void*)dist,theta[4],theta[2],
                         pdf1*1e-6,1e-9*(theta[2]-theta[4]),&warnz[3]);
 
        theta[0]=theta[1];
        break;

      default: // Nunca llegara aqui
        theta[1] = 0.5*(theta[4]-theta[2]);
        theta[3] = 0.5*(theta[2]+theta[0]);
        break;
    }

  #ifdef DEBUG
  aux_eval=integ_eval;
  integ_eval=0;
  #endif

  stable_integration(dist,integrando,theta[1],theta[2],
                             absTOL,relTOL,IT_MAX,
                             &pdf_aux,&err_aux,METHOD1);
  pdf1=fabs(pdf_aux);
  *err=err_aux*err_aux;

  #ifdef DEBUG
  warnz[0]=integ_eval;
  integ_eval=0;
  #endif

  stable_integration(dist,integrando,theta[2],theta[3],
                             max(pdf1*relTOL,absTOL)*0.25,relTOL,IT_MAX,
                             &pdf_aux,&err_aux,METHOD2);
  pdf2=fabs(pdf_aux);
  *err+=err_aux*err_aux;
  #ifdef DEBUG
  warnz[1]=integ_eval;
  integ_eval=0;
  #endif

  stable_integration(dist,integrando,theta[3],theta[4],
                            max((pdf2+pdf1)*relTOL,absTOL)*0.25,relTOL,IT_MAX,
                            &pdf_aux,&err_aux,METHOD3);
  pdf3=fabs(pdf_aux);
  *err+=err_aux*err_aux;
  #ifdef DEBUG
  warnz[2]=integ_eval;
  integ_eval=0;
  #endif

  stable_integration(dist,integrando,theta[0],theta[1],
                             max((pdf3+pdf2+pdf1)*relTOL,absTOL)*0.25,relTOL,IT_MAX,
                             &pdf_aux,&err_aux,STABLE_QAG2);
  *err+=err_aux*err_aux;


  //Sumar de menor a mayor contribucion para minimizar error de redondeo.
  pdf=fabs(pdf_aux)+pdf3+pdf2+pdf1;
  //pdf3=0;
  //pdf_aux=0;
  //warnz[2]=0;
  //pdf=pdf2+pdf1;
  *err=sqrt(*err)/pdf;

  #ifdef DEBUG
  fprintf(FINTEG,"%+1.3e % 1.3e % 1.3e",x,pdf,*err);
  fprintf(FINTEG," %+1.3e %+1.3e %+1.3e %+1.3e %+1.3e",theta[0],theta[1],theta[2],theta[3],theta[4]);
  fprintf(FINTEG," % 1.3e % 1.3e % 1.3e % 1.3e", pdf1,pdf2,pdf3,fabs(pdf_aux));
  fprintf(FINTEG," %d %d %d %d %d %d\n",
          warnz[0],warnz[1],warnz[2],integ_eval,aux_eval,
          warnz[0]+warnz[1]+warnz[2]+integ_eval+aux_eval);
  printf("abstols % 1.3e % 1.3e % 1.3e % 1.3e \n",absTOL,max(pdf1*relTOL,absTOL)*0.5,max((pdf2+pdf1)*relTOL,absTOL)*0.25,max((pdf3+pdf2+pdf1)*relTOL,absTOL)*0.25);

  #endif

  return pdf;
}

/******************************************************************************/
/*   PDF de casos particulares                                                */
/******************************************************************************/

double
stable_pdf_point_GAUSS(StableDist *dist, const double x, double *err)
{
  double x_=(x-dist->mu_0)/dist->sigma;
  *err = 0.0;

  return 0.5*sqrt(M_1_PI)/dist->sigma*exp(-x_*x_*0.25);
}

double
stable_pdf_point_CAUCHY(StableDist *dist, const double x, double *err)
{
  double x_=(x-dist->mu_0)/dist->sigma;
  *err = 0.0;

  return M_1_PI/(1+x_*x_)/dist->sigma;
}   

double
stable_pdf_point_LEVY(StableDist *dist, const double x, double *err)
{
  double xxi=(x-dist->mu_0)/dist->sigma-dist->xi;
  *err=0.0;

  if (xxi>0 && dist->beta>0)
    return sqrt(dist->sigma*0.5*M_1_PI) *
           exp(-dist->sigma*0.5/(xxi*dist->sigma)) /
           pow(xxi*dist->sigma,1.5);
  else if (xxi<0 && dist->beta<0)
    return sqrt(dist->sigma*0.5*M_1_PI) *
           exp(-dist->sigma*0.5/(fabs(xxi)*dist->sigma)) /
           pow(fabs(xxi)*dist->sigma,1.5);
  else return 0.0;
}

/******************************************************************************/
/*   PDF en otros casos                                                       */
/******************************************************************************/

double
stable_pdf_point_PEQXXIP(StableDist *dist, const double x, double *err)
{
/* Este caso se da en:
       x ~ xi  con alpha > 1
       x >> xi con alpha < 1
       x << 0  con alpha = 1 y beta < 0
       x >> 0  con alpha = 1 y beta > 0 */

/* Estrategia:
     - Busca el máximo del integrando: theta[2]
     - 1 - Integra en intervalo simetrico entorno al maximo
     - 2 - Integra el resto que queda por encima del umbral
     - Suma todo */
  return 0.0;
}

double
stable_pdf_point_MEDXXIP(StableDist *dist, const double x, double *err)
{
  return 0.0;
}

double
stable_pdf_point_ALPHA_1(StableDist *dist, const double x, double *err)
{
  double pdf=0;
  double x_;//, xxi;

  #ifdef DEBUG
  integ_eval=0;
  #endif

  x_=(x-dist->mu_0)/dist->sigma;
  //xxi=x_-dist->xi;
  dist->beta_ = dist->beta;

  if (dist->beta < 0.0)
    {
      x_ = -x_;
      dist->beta_ = -dist->beta;
    }

  else {dist->beta_ = dist->beta;}

  dist->xxipow = (-M_PI*x_*dist->c2_part);

  pdf = stable_integration_pdf(dist,&stable_pdf_g1,&stable_g_aux1,err);
  pdf = dist->c2_part*pdf;
  return pdf/dist->sigma;
}

double stable_pdf_point_STABLE(StableDist *dist, const double x, double *err)
{
  double pdf=0;
  double x_, xxi;

  #ifdef DEBUG
  int aux_eval=0;
  integ_eval=0;
  #endif

  x_=(x-dist->mu_0)/dist->sigma;
  xxi=x_-dist->xi;

  /*Si justo evaluo en o cerca de xi interpolacion lineal*/
  //xxi_th = XXI_TH*(1.0+fabs(dist->alphainvalpha1-1.0));

  if (fabs(xxi) <= XXI_TH)
    {
      *err=0;
//      printf("_%lf_\n",x);
      pdf = exp(gammaln(1.0+1.0/dist->alpha)) *
            cos(dist->theta0)/(M_PI*dist->S);
/*
      if (xxi>0) pdf1 = stable_pdf_point(dist,(dist->xi+1.01*xxi_th)*dist->sigma,err);
      else if(xxi==0) pdf1=pdf;
      else pdf1 = stable_pdf_point(dist,(dist->xi-1.01*xxi_th)*dist->sigma,err);

      pdf = pdf*(1-fabs(xxi)/(xxi_th*1.01))+pdf1*fabs(xxi)/(xxi_th*1.01);
 */

      #ifdef DEBUG
      printf("Aproximando x a zeta para alpha = %f, beta = %f, zeta = %f : pdf = %f\n",
               dist->alpha,dist->beta,dist->xi,pdf);
            
      fprintf(FINTEG,"%1.3e\t%1.3e\t%1.3e\t%1.3e\t%1.3e\t%1.3e\t%d\t%d\t%d\t%d\n",
              x,pdf,*err,0.0,0.0,0.0,aux_eval,0,aux_eval,aux_eval<<1);
      #endif
      return pdf/dist->sigma;
    }
  else if (xxi<0)   /* pdf(x<xi,a,b) = pdf(-x,a,-b)*/
    { 
      xxi=-xxi;
      dist->theta0_=-dist->theta0; /*theta0(a,-b)=-theta0(a,b)*/
      dist->beta_=-dist->beta;
    }
  else
    {
      dist->theta0_=dist->theta0;
      dist->beta_=dist->beta;
    }
  dist->xxipow=dist->alphainvalpha1*log(fabs(xxi));

  /*Si theta0~=-PI/2 intervalo de integración nulo*/
  /*incluye a beta=+-1 y alpha<1->pdf nula a la izqda/dcha de xi*/
  if (fabs(dist->theta0_+M_PI_2)<2*THETA_TH)
    {
     #ifdef DEBUG
      printf("Intervalo de integracion nulo\n");
     #endif

     return 0.0;
    }
  
//  if (dist->xxipow > XXIPOWMAX)
//    {
  pdf = stable_integration_pdf(dist,&stable_pdf_g2,&stable_g_aux2,err);
//    }
//  else if (dist->xxipow < XXIPOWMIN)
//    {
//      pdf = stable_pdf_point_PEQXXIP(dist,x,err)
//    }
//  else
//    {
//    }

  pdf = dist->c2_part/xxi*pdf;

  return pdf/dist->sigma;
}

/******************************************************************************/
/*   PDF point en general                                                     */
/******************************************************************************/

double
stable_pdf_point(StableDist *dist, const double x, double *err)
{
  double temp;

  if (err==NULL) err=&temp;

  return (dist->stable_pdf_point)(dist,x,err);
}
