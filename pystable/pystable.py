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


def create(alpha: float, beta: float, sigma: float, mu: float,
           parameterization: int, path=None) -> STABLE_DIST:
    lib = load_libstable(path)
    return stable_create(lib, alpha, beta, sigma, mu, parameterization)


def stable_create(lib: ct.CDLL, alpha: float, beta: float, sigma: float,
                  mu: float, parameterization: int) -> STABLE_DIST:
    c_fn = c_stable_create(lib)
    return c_fn(alpha, beta, sigma, mu, parameterization)


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


def checkparams(alpha: float, beta: float, sigma: float, mu: float,
                parameterization: int, path=None) -> int:
    lib = load_libstable(path)
    return stable_checkparams(lib, alpha, beta, sigma, mu, parameterization)


def stable_checkparams(lib: ct.CDLL, alpha: float, beta: float, sigma: float,
                       mu: float, parameterization: int) -> int:
    c_fn = c_stable_checkparams(lib)
    return c_fn(alpha, beta, sigma, mu, parameterization)


def c_stable_checkparams(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.c_double, ct.c_double, ct.c_double, ct.c_double, ct.c_int)
    ret = ct.c_int
    return wrap_function(lib, 'stable_checkparams', ret, args)


def cdf(dist: STABLE_DIST, x: tp.List[float], Nx: int,
        path=None) -> tp.List[float]:
    lib = load_libstable(path)
    return stable_cdf(lib, dist, x, Nx)


def stable_cdf(lib: ct.CDLL, dist: STABLE_DIST, x: tp.List[float],
               Nx: int) -> tp.List[float]:
    c_fn = c_stable_cdf(lib)
    array_type = ct.c_double * Nx
    LP_c_double = ct.POINTER(ct.c_double)
    cdf = (ct.c_double * Nx)()
    c_fn(dist, array_type(*x), Nx, cdf, LP_c_double())
    return list(cdf)


def c_stable_cdf(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint,
            ct.POINTER(ct.c_double), ct.POINTER(ct.c_double))
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_cdf', ret, args)


def cdf_point(dist: STABLE_DIST, x: float, path=None):
    lib = load_libstable(path)
    return stable_cdf_point(lib, dist, x)


def stable_cdf_point(lib: ct.CDLL, dist: STABLE_DIST, x: float):
    c_fn = c_stable_cdf_point(lib)
    LP_c_double = ct.POINTER(ct.c_double)
    return c_fn(dist, x, LP_c_double())


def c_stable_cdf_point(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.c_double, ct.POINTER(ct.c_double))
    ret = ct.c_double
    return wrap_function(lib, 'stable_cdf_point', ret, args)


def fit(dist: STABLE_DIST, data: tp.List[float], length: int,
        path=None) -> int:
    lib = load_libstable(path)
    return stable_fit(lib, dist, data, length)


def stable_fit(lib: ct.CDLL, dist: STABLE_DIST, data: tp.List[float],
               length: int) -> int:
    c_fn = c_stable_fit(lib)
    array_type = ct.c_double * length
    return c_fn(dist, array_type(*data), length)


def c_stable_fit(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint)
    ret = ct.c_int
    return wrap_function(lib, 'stable_fit', ret, args)


def pdf(dist: STABLE_DIST, x: tp.List[float], Nx: int,
        path=None) -> tp.List[float]:
    lib = load_libstable(path)
    return stable_pdf(lib, dist, x, Nx)


def stable_pdf(lib: ct.CDLL, dist: STABLE_DIST, x: tp.List[float],
               Nx: int) -> tp.List[float]:
    c_fn = c_stable_pdf(lib)
    array_type = ct.c_double * Nx
    LP_c_double = ct.POINTER(ct.c_double)
    pdf = (ct.c_double * Nx)()
    c_fn(dist, array_type(*x), Nx, pdf, LP_c_double())
    return list(pdf)


def c_stable_pdf(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint,
            ct.POINTER(ct.c_double), ct.POINTER(ct.c_double))
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_pdf', ret, args)


def q(dist: STABLE_DIST, q: tp.List[float], Nq: int,
      path=None) -> tp.List[float]:
    lib = load_libstable(path)
    return stable_q(lib, dist, q, Nq)


def stable_q(lib: ct.CDLL, dist: STABLE_DIST, q: tp.List[float],
             Nq: int) -> tp.List[float]:
    c_fn = c_stable_q(lib)
    array_type = ct.c_double * Nq
    LP_c_double = ct.POINTER(ct.c_double)
    inv = (ct.c_double * Nq)()
    c_fn(dist, array_type(*q), Nq, inv, LP_c_double())
    return list(inv)


def c_stable_q(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint,
            ct.POINTER(ct.c_double), ct.POINTER(ct.c_double))
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_q', ret, args)


def rnd(dist: STABLE_DIST, n: int, path=None) -> tp.List[float]:
    lib = load_libstable(path)
    return stable_rnd(lib, dist, n)


def stable_rnd(lib: ct.CDLL, dist: STABLE_DIST, n: int) -> tp.List[float]:
    c_fn = c_stable_rnd(lib)
    array_type = ct.c_double * n
    rnd = (ct.c_double * n)()
    c_fn(dist, array_type(*rnd), n)
    return list(rnd)


def c_stable_rnd(lib: ct.CDLL) -> ct.CDLL._FuncPtr:
    args = (ct.POINTER(STABLE_DIST), ct.POINTER(ct.c_double), ct.c_uint)
    ret = ct.c_void_p
    return wrap_function(lib, 'stable_rnd', ret, args)
