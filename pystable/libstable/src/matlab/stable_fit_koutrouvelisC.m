function [pars, status]=stable_fit_koutrouvelisC(data, pars_init, parametrization)
% [pars, status] = stable_fit_koutrouvelisC(data, pars_init, parametrization)
% Koutrouvelis [1] estimation of alpha-stable parameters.
%  Inputs:
%    data:  vector of random data
%    pars_init:    initial guess of parameters estimation. If none is provided,
%           McCulloch estimation is done before ML.
%    parametrization:  parameterization employed (view [1] for details)
%             0:   mu=mu_0
%             1:   mu=mu_1
%  Outputs:
%    pars = [alpha,beta,sigma,mu_0]. Estimated parameters.
%    status : status>0 indicates some error on the iterative procedure.
%
% Copyright (C) 2013. Javier Royuela del Val
%                     Federico Simmross Wattenberg
%
% [1] Ioannis A. Koutrouvelis. An iterative procedure for the estimation of the
%     parameters of stable laws. Communications in Statistics - Simulation and
%     Computation, 10(1):17–28, 1981.

% This program is free software; you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation; version 3 of the License.
% 
% This program is distributed in the hope that it will be useful, but
% WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
% General Public License for more details.
% 
% You should have received a copy of the GNU General Public License
% along with this program; If not, see <http://www.gnu.org/licenses/>.
%
%
%  Javier Royuela del Val.
%  E.T.S.I. Telecomunicación
%  Universidad de Valladolid
%  Paseo de Belén 15, 47002 Valladolid, Spain.
%  jroyval@lpi.tel.uva.es    
%

if nargin < 3
    parametrization = 0;
end
if nargin < 2
    pars_init = [];
end

if (parametrization<0 || parametrization >1)
    error('parametrization must be 0 or 1');
end

pnu_c=0;pnu_z=0;
n=length(data);

if nargin < 3
    parametrization = 0;
end

if nargin < 2
    pars_init = [];
end

if ~isempty(pars_init)
    dist=calllib('libstable','stable_create', ...
        pars_init(1),pars_init(2),pars_init(3),pars_init(4),parametrization); 
else
    dist=calllib('libstable','stable_create',1,0,1,0,0);
    calllib('libstable','stable_fit_init',dist,data,n,pnu_c,pnu_z);
end

calllib('libstable','stable_set_THREADS', 0);
calllib('libstable','stable_set_relTOL', 1e-8);
calllib('libstable','stable_set_absTOL', 1e-8);

status=calllib('libstable','stable_fit_koutrouvelis', dist, data, n);

if parametrization == 0
    mu = dist.Value.mu_0;
elseif parametrization == 1
    mu = dist.Value.mu_1;
else
    warning('Wrong parametrization used. Returning mu_0 by default');
    mu = dist.Value.mu_0;
end

pars=[dist.Value.alpha dist.Value.beta dist.Value.sigma mu];

calllib('libstable','stable_free',dist);
