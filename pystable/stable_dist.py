import ctypes as ct


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
