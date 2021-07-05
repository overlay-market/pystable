from ctypes import *
import os

LIBSTABLE_PATH = 'libstable/stable/libs/libstable.so'

#  def read_helpers(file_name):
#      df = pd.read_csv(path)

def libstable_path():
    '''Get path to libstable.so'''
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    return os.path.abspath(os.path.join(path, LIBSTABLE_PATH))

#  /* Parameters:
#  0-parametrization describen in Nolan, 1997 is employed by default
#      alpha : stability index
#      beta : skewness parameter
#      scale: scale parameter
#      mu_0 : 0-parametrization location parameter
#      mu_1 : correspondig 1-parametrization location parameter    */
class STABLE_DIST(Structure):
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
    '''Create `StableDist` struct by calling `stable_create`'''
    c_stable_create_args = (c_double,
                            c_double,
                            c_double,
                            c_double,
                            c_int)

    c_stable_create_ret = POINTER(STABLE_DIST)

    c_stable_create = wrap_function(lib,
                                    'stable_create',
                                    c_stable_create_ret,
                                    c_stable_create_args)

    return c_stable_create(params['alpha'], params['beta'], params['mu'], params['sigma'], params['parameterization'])


if __name__ == "__main__":
    path = libstable_path()
    lib = cdll.LoadLibrary(path)

    # Test a C call
    pf = lib.printf
    pf(b'hi, %s\n', b'world')

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

    # Working `stable_create` with dummy variables
    dist_params_dummy = {
            'alpha': 2.0,
            'beta': 0.0,
            'mu': 1.0, # loc
            'sigma': 0.0, # scale
            'parameterization': 0,
        }

    dist_working = stable_create(lib, dist_params_dummy)
    print('Dummy params working:')
    print(dist_working.contents)
    print('\talpha: ', dist_working.contents.alpha)
    print('\tbeta: ', dist_working.contents.beta)
    print('\tmu_0: ', dist_working.contents.mu_0)
    print('\tmu_1: ', dist_working.contents.mu_1)


    # Not working `stable_create` with variables from https://github.com/overlay-market/pystable/blob/tests/tests/helpers/fit.csv
    dist_params = {
            'alpha': 1.3278285879842862,
            'beta': 0.0816835526225623,
            'mu': -0.0000252748167384907, # loc
            'sigma': 0.0006409442772706084, # scale
            'parameterization': 1,
        }

    dist_not_working = stable_create(lib, dist_params)
    print(dist_not_working.contents)    # NULL pointer access error
    #  print(dist_not_working.contents.alpha)

