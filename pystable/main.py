import pandas as pd
from ctypes import *
import os

LIBSTABLE_PATH = 'libstable/stable/libs/libstable.so'

def read_helpers(file_name):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    path = os.path.abspath(os.path.join(path, 'tests/helpers'))
    path = os.path.abspath(os.path.join(path, file_name))

    return pd.read_csv(path)

def libstable_path():
    '''Get path to libstable.so'''
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    return os.path.abspath(os.path.join(path, LIBSTABLE_PATH))

class STABLE_DIST(Structure):
    '''
    Stable distribution structure.

    Parameters:
      alpha [c_double]:  Stability index
      beta  [c_double]:  Skewness parameter
      scale [c_double]:  Scale parameter
      mu_0  [c_double]:  0-parametrization local parameter
      mu_1  [c_double]:  corresponding 1-parametrization local parameter
    '''
    _fields_ = [('alpha', c_double),
                ('beta', c_double),
                ('sigma', c_double),
                ('mu_0', c_double),
                ('mu_1', c_double)]

def wrap_function(lib, funcname, restype, argtypes):
    '''Wrap ctypes functions'''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func

def stable_checkparams(lib, params):
    # RR TODO
    # Test `stable_checkparams` in stable_dist.c
    s_cp_args = (c_double,
                 c_double,
                 c_double,
                 c_double,
                 c_int)
    s_cp_ret = c_int

    s_cp = wrap_function(lib, 'stable_checkparams', s_cp_ret, s_cp_args)
    a = s_cp(1.0, 0.5, 1.5, 1.5, 5)
    #  print(a)

def stable_create(lib, params):
    dist = c_stable_create(lib, params).contents
    return {
              'alpha': dist.alpha,
              'beta': dist.beta,
              'sigma': dist.sigma,
              'mu_0': dist.mu_0,
              'mu_1': dist.mu_1,
            }

def c_stable_create(lib, params):
    '''
    Call `stable_create` function to create a `StableDist` struct.

    Inputs:
      lib    [CDLL]:  libstable dynamically linked library
      params [Dict]:  `stable_create` input arguments
        alpha            [double]:
        beta             [double]:
        mu               [double]:
        sigma            [double]:
        parameterization [int]:

    Outputs:
        [Stable_DIST object]: contains resulting `StableDist` struct parameters
          alpha [double]:
          beta  [double]:
          mu_0  [double]:
          mu_1  [double]:
    '''
    args = (c_double, c_double, c_double, c_double, c_int)
    ret = POINTER(STABLE_DIST)
    c_fn = wrap_function(lib, 'stable_create', ret, args)

    return c_fn(params['alpha'], params['beta'], params['sigma'],
                           params['mu'], params['parameterization'])

def stable_cdf(lib, params):
    c_fn = c_stable_cdf(lib, params)
    array_type = c_double * params['Nx']
    LP_c_double = POINTER(c_double)
    cdf = (c_double * params['Nx'])()

    c_fn(params['dist'], array_type(*params['x']), params['Nx'], cdf,
               LP_c_double())

    return list(cdf)

def c_stable_cdf(lib, params):
    array_type = c_double * params['Nx']
    args = (POINTER(STABLE_DIST), POINTER(c_double), c_uint,
            POINTER(c_double), POINTER(c_double))
    ret = c_void_p
    return wrap_function(lib, 'stable_cdf', ret, args)

def stable_cdf_point(lib, params):
    c_fn = c_stable_cdf_point(lib, params)
    LP_c_double = POINTER(c_double)
    return c_fn(params['dist'], params['x'], LP_c_double())

def c_stable_cdf_point(lib, params):
    args = (POINTER(STABLE_DIST), c_double, POINTER(c_double))
    ret = c_double
    return wrap_function(lib, 'stable_cdf_point', ret, args)

if __name__ == "__main__":
    path = libstable_path()
    lib = cdll.LoadLibrary(path)

    # Test example C `our_function` call
    pys_our_fn = lib.our_function.argtypes = (c_int, POINTER(c_int))
    numbers = [1, 2, -3, 4, -5, 6]
    num_numbers = len(numbers)
    array_type = c_int * num_numbers
    result = lib.our_function(c_int(num_numbers), array_type(*numbers))
    print(int(result))
    print()


    # `create_stable` input args to create pointer to `StableDist` struct
    dist_params = {
            'alpha': 1.3278285879842862,
            'beta': 0.0816835526225623,
            'mu': -0.0000252748167384907, # loc
            'sigma': 0.0006409442772706084, # scale
            'parameterization': 1,
        }

    dist = c_stable_create(lib, dist_params)
    dist_params = stable_create(lib, dist_params)
    
    stable_cdf_point_params = {
              'dist': dist, 
              'x': -0.009700000000000002,
            }
    ret = stable_cdf_point(lib, stable_cdf_point_params)
    print(ret)

    df_params = read_helpers('cdfs.csv')
    x = []
    for i in df_params['x']:
        x.append(i)
    Nx = len(x)
    cdf = [0] * Nx
    cdf_params = {
            'dist': dist,
            'x': x,
            'Nx': Nx,
            'cdf': cdf,
        }

    cdf = stable_cdf(lib, cdf_params)
    print(cdf)
    print(len(cdf))
