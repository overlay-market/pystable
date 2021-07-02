function rnd = stable_rndC(n, pars, parametrization, seed)
% rnd = stable_rndC(n, pars, parametrization, seed)
% Random sample generation of alpha-stable random variable.
%  Inputs:
%    pars:   parameters of the alpha-estable distributions.
%                  pars=[alpha,beta,sigma,mu];
%    n:      size of the random sample.
%    parametrization:  parameterization employed (view [1] for details)
%             0:   mu=mu_0
%             1:   mu=mu_1
%    seed:   random seed. If omitted, one is generated based on system time
%
% [1] Nolan, J. P. Numerical Calculation of Stable Densities and
%     Distribution Functions Stochastic Models, 1997, 13, 759-774
%
% Copyright (C) 2013. Javier Royuela del Val
%                     Federico Simmross Wattenberg

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

if nargin < 4 || isempty('seed') || seed==0
    seed = floor(rem(now,1)*86400*1e9);
end
if nargin < 3
    parametrization = 0;
end
if nargin < 2
    pars = [2, 0, 1, 0];
end

if length(pars) ~= 4
    error('pars must be a four elements vector');
end
if (parametrization<0 || parametrization >1)
    error('parametrization must be 0 or 1');
end

dist=calllib('libstable','stable_create',pars(1),pars(2),pars(3),pars(4),parametrization);


calllib('libstable','stable_rnd_seed',dist,seed);

rnd=zeros(1,n);
[~,rnd]=calllib('libstable','stable_rnd',dist,rnd,n);


calllib('libstable','stable_free',dist);
