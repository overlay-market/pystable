import ctypes as ct
import os
import pandas as pd
import pystable
import unittest


class TestPystable(unittest.TestCase):
    def setUp(self):
        self.lib = pystable.load_libstable()
        self.dist_params = self.get_helper('fit.csv')

    def get_helpers(self, file_name: str):
        '''Retrieves helpers csv file'''
        file_name = '{}.csv'.format(file_name)
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.abspath(os.path.join(path, 'helpers'))
        path = os.path.abspath(os.path.join(path, file_name))

        return pd.read_csv(path)

    def get_fn_params(self, fn_name: str, dist):
        df_params = self.get_helpers(fn_name)
        x = []
        for i in df_params['x']:
            x.append(i)
        Nx = len(x)
        fn_data = [0] * Nx
        return {
                'dist': dist,
                'x': x,
                'Nx': Nx,
                'fn': fn_data,
            }

    def get_helper(self, name) -> str:
        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, 'helpers')
        base = os.path.join(base, name)
        return pd.read_csv(base).to_dict(orient='records')[0]

    def test_c_stable_checkparams(self):
        expected_args = (ct.c_double, ct.c_double, ct.c_double, ct.c_double,
                         ct.c_int)
        actual = pystable.c_stable_checkparams(self.lib)

        self.assertEqual('stable_checkparams', actual.__name__)
        self.assertEqual(expected_args, actual.argtypes)
        self.assertEqual(ct.c_int, actual.restype)

    def test_stable_checkparams(self):
        actual = pystable.stable_checkparams(self.lib, self.dist_params)
        self.assertEqual(0, actual)

    def test_stable_checkparams_err(self):
        pass

    def test_c_stable_create(self):
        expected_args = (ct.c_double, ct.c_double, ct.c_double, ct.c_double,
                         ct.c_int)
        expected_res = ct.POINTER(pystable.STABLE_DIST)
        actual = pystable.c_stable_create(self.lib)

        self.assertEqual('stable_create', actual.__name__)
        self.assertEqual(expected_args, actual.argtypes)
        self.assertEqual(expected_res, actual.restype)

    def test_stable_create(self):
        # TODO: `mu_0` gets truncated on pandas csv read from
        # `helpers/stable_create.csv`
        #  expected = self.get_helper('stable_create.csv')
        expected = {
                'alpha': 1.3278285879842862,
                'beta': 0.0816835526225623,
                'sigma': 0.0006409442772706,
                'mu_0': -0.00011779403879886721,
                'mu_1': -2.52748167384e-05
                }
        actual = pystable.stable_create(self.lib, self.dist_params)

        self.assertEqual(expected['alpha'], actual.contents.alpha)
        self.assertEqual(expected['beta'], actual.contents.beta)
        self.assertEqual(expected['sigma'], actual.contents.sigma)
        self.assertEqual(expected['mu_0'], actual.contents.mu_0)
        self.assertEqual(expected['mu_1'], actual.contents.mu_1)
