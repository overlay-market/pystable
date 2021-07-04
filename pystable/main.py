import ctypes
import os

LIBSTABLE_PATH = 'libstable/stable/libs/libstable.so'

class STABLE_DIST(ctypes.Structure):
    _fields_ = [('alpha', ctypes.c_double),
                ('beta', ctypes.c_double),
                ('sigma', ctypes.c_double),
                ('mu_0', ctypes.c_double),
                ('mu_1', ctypes.c_double)]

def libstable_path():
    '''Get path to libstable.so'''
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    return os.path.abspath(os.path.join(path, LIBSTABLE_PATH))

def wrap_function(lib, funcname, restype, argtypes):
    '''Wrap ctypes functions'''
    func = lib.__getattr__(funcname)
    func.restype = restype
    func.argtypes = argtypes
    return func

if __name__ == "__main__":
    path = libstable_path()
    lib = ctypes.cdll.LoadLibrary(path)

    # Test a C call
    pf = lib.printf
    pf(b'hi, %s\n', b'world')

    # Test example C `our_function` call
    pys_our_fn = lib.our_function.argtypes = (ctypes.c_int, ctypes.POINTER(ctypes.c_int))
    numbers = [1, 2, -3, 4, -5, 6]
    num_numbers = len(numbers)
    array_type = ctypes.c_int * num_numbers
    result = lib.our_function(ctypes.c_int(num_numbers), array_type(*numbers))
    print(int(result))
    print()

    # Test `stable_checkparams` in stable_dist.c
    s_cp_args = (ctypes.c_double,
                 ctypes.c_double,
                 ctypes.c_double,
                 ctypes.c_double,
                 ctypes.c_int)
    s_cp_ret = ctypes.c_int

    s_cp = wrap_function(lib, 'stable_checkparams', s_cp_ret, s_cp_args)
    a = s_cp(1.0, 0.5, 1.5, 1.5, 5)
    print(a)


    c_stable_create_args = (ctypes.c_double,
                            ctypes.c_double,
                            ctypes.c_double,
                            ctypes.c_double,
                            ctypes.c_int)

    c_stable_create_ret = ctypes.POINTER(STABLE_DIST)

    c_stable_create = wrap_function(lib,
                                    'stable_create',
                                    c_stable_create_ret,
                                    c_stable_create_args)

    print(dir(c_stable_create))
    print(c_stable_create)

    dist = c_stable_create(2.0, 0.0, 1.0, 0.0, 0)
    print(dir(dist))
