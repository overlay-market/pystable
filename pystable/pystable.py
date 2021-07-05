import utils
import ctypes as ct


def load_libstable():
    return ct.cdll.LoadLibrary(utils.libstable_path())


class STABLE_DIST(ct.Structure):
    '''
    Stable distribution structure.

    Parameters:
      alpha [ct.c_double]:  Stability index
      beta  [ct.c_double]:  Skewness parameter
      scale [ct.c_double]:  Scale parameter
      mu_0  [ct.c_double]:  0-parametrization local parameter
      mu_1  [ct.c_double]:  corresponding 1-parametrization local parameter
    '''
    _fields_ = [('alpha', ct.c_double),
                ('beta', ct.c_double),
                ('sigma', ct.c_double),
                ('mu_0', ct.c_double),
                ('mu_1', ct.c_double)]


def wrap_function(lib, funcname, restype, argtypes):
    '''Wrap ctypes functions'''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


def stable_checkparams(lib, params):
    args = (ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_int)
    ret = ct.c_int
    c_fn = wrap_function(lib, 'stable_checkparams', ret, args)
    a = c_fn(1.0, 0.5, 1.5, 1.5, 5)
    print(a)


def stable_create(lib, params):
    c_fn = c_stable_create(lib, params)
    return c_fn(params['alpha'], params['beta'], params['sigma'], params['mu'],
                params['parameterization'])


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
    args = (ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_int)
    ret = ct.POINTER(STABLE_DIST)
    return wrap_function(lib, 'stable_create', ret, args)


def stable_cdf(lib, params):
    c_fn = c_stable_cdf(lib, params)
    array_type = ct.c_double * params['Nx']
    LP_c_double = ct.POINTER(ct.c_double)
    cdf = (ct.c_double * params['Nx'])()

    c_fn(params['dist'], array_type(*params['x']), params['Nx'], cdf,
         LP_c_double())

    return list(cdf)


def c_stable_cdf(lib, params):
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint,
            ct.POINTER(ct.c_double), ct.POINTER(ct.c_double))
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_cdf', ret, args)


def stable_cdf_point(lib, params):
    c_fn = c_stable_cdf_point(lib, params)
    LP_c_double = ct.POINTER(ct.c_double)
    return c_fn(params['dist'], params['x'], LP_c_double())


def c_stable_cdf_point(lib, params):
    args = (ct.POINTER(STABLE_DIST), ct.c_double, ct.POINTER(ct.c_double))
    ret = ct.c_double
    return wrap_function(lib, 'stable_cdf_point', ret, args)
