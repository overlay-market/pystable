from ctypes import *
import os

LIBSTABLE_PATH = 'libstable/stable/libs/libstable.so'

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

def stable_create(lib, params):
    dist = c_stable_create(lib, params).contents
    return {
              'alpha': dist.alpha,
              'beta': dist.beta,
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

    # `create_stable` input args to create pointer to `StableDist` struct
    dist_params = {
            'alpha': 1.3278285879842862,
            'beta': 0.0816835526225623,
            'mu': -0.0000252748167384907, # loc
            'sigma': 0.0006409442772706084, # scale
            'parameterization': 1,
        }
    dist = stable_create(lib, dist_params)
    print(dist)
