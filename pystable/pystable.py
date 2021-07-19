import ctypes as ct
import typing as tp
from pystable.stable_dist import STABLE_DIST
from pystable import utils


def load_libstable(libstable_path=None) -> ct.CDLL:
    '''
    Load the C libstable DLL
    Inputs:
        libstable_path [str]: Optional path to `libstable.so`. Default path is
                              `pystable/_extensions/libstable.so`
    Outputs:
        [ct.CDLL]:            Dynamically linked libstable library
    '''
    if libstable_path:
        return ct.cdll.LoadLibrary(libstable_path)
    else:
        return ct.cdll.LoadLibrary(utils.libstable_path())


def wrap_function(lib: ct.CDLL, funcname: str, restype, argtypes
                  ) -> ct.CDLL._FuncPtr:
    '''Wrap ctypes functions'''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func


def stable_create(lib: ct.CDLL, params: tp.Dict) -> STABLE_DIST:
    c_fn = c_stable_create(lib)
    return c_fn(params['alpha'], params['beta'], params['sigma'], params['mu'],
                params['parameterization'])


def c_stable_create(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    '''
    Call `stable_create` function to create a `StableDist` struct.

    Inputs:
      lib    [ct.CDLL]:  libstable dynamically linked library

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


def stable_checkparams(lib: ct.CDLL, params) -> int:
    c_fn = c_stable_checkparams(lib)
    return c_fn(params['alpha'], params['beta'], params['sigma'], params['mu'],
                params['parameterization'])


def c_stable_checkparams(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_int)
    ret = ct.c_int
    return wrap_function(lib, 'stable_checkparams', ret, args)


def stable_cdf(lib: ct.CDLL, params: tp.Dict) -> tp.List[float]:
    c_fn = c_stable_cdf(lib)
    array_type = ct.c_double * params['Nx']
    LP_c_double = ct.POINTER(ct.c_double)
    cdf = (ct.c_double * params['Nx'])()

    c_fn(params['dist'], array_type(*params['x']), params['Nx'], cdf,
         LP_c_double())

    return list(cdf)


def c_stable_cdf(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint,
            ct.POINTER(ct.c_double), ct.POINTER(ct.c_double))
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_cdf', ret, args)


def stable_cdf_point(lib: ct.CDLL, params: tp.Dict):
    c_fn = c_stable_cdf_point(lib)
    LP_c_double = ct.POINTER(ct.c_double)
    return c_fn(params['dist'], params['x'], LP_c_double())


def c_stable_cdf_point(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.c_double, ct.POINTER(ct.c_double))
    ret = ct.c_double
    return wrap_function(lib, 'stable_cdf_point', ret, args)


def stable_fit(lib: ct.CDLL, params: tp.Dict) -> int:
    c_fn = c_stable_fit(lib)
    array_type = ct.c_double * params['length']
    return c_fn(params['dist'], array_type(*params['data']), params['length'])


def c_stable_fit(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint)
    ret = ct.c_int
    return wrap_function(lib, 'stable_fit', ret, args)


def stable_pdf(lib: ct.CDLL, params: tp.Dict) -> tp.List[float]:
    c_fn = c_stable_pdf(lib)
    array_type = ct.c_double * params['Nx']
    LP_c_double = ct.POINTER(ct.c_double)
    pdf = (ct.c_double * params['Nx'])()

    c_fn(params['dist'], array_type(*params['x']), params['Nx'], pdf,
         LP_c_double())

    return list(pdf)


def c_stable_pdf(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint,
            ct.POINTER(ct.c_double), ct.POINTER(ct.c_double))
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_pdf', ret, args)


def stable_q(lib: ct.CDLL, params: tp.Dict) -> tp.List[float]:
    c_fn = c_stable_q(lib)
    array_type = ct.c_double * params['Nq']
    LP_c_double = ct.POINTER(ct.c_double)
    q = (ct.c_double * params['Nq'])()

    c_fn(params['dist'], array_type(*params['q']), params['Nq'], q,
         LP_c_double())

    return list(q)


def c_stable_q(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint,
            ct.POINTER(ct.c_double), ct.POINTER(ct.c_double))
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_q', ret, args)


def stable_rnd(lib: ct.CDLL, params: tp.Dict) -> tp.List[float]:
    c_fn = c_stable_rnd(lib)
    array_type = ct.c_double * params['rnd']
    rnd = (ct.c_double * params['n'])()

    c_fn(params['dist'], array_type(*params['rnd']), params['n'])

    return list(rnd)


def c_stable_rnd(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint)
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_rnd', ret, args)
