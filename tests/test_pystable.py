import os
import ctypes as ct
import pandas as pd
import numpy as np
import unittest
import pystable


class TestPystable(unittest.TestCase):

    def get_fit(self):
        '''Get fit dist parameter'''
        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, 'helpers/fit.csv')
        return pd.read_csv(base).to_dict(orient='records')[0]

    def test_stable_checkparams(self):
        '''
        Test `stable_checkparams` high-level function.
        `stable_checkparams` returns 0 on success.
        '''
        lib = pystable.load_libstable()
        params = self.get_fit()
        actual = pystable.stable_checkparams(lib, params)
        self.assertEqual(0, actual)

    def test_c_stable_checkparams(self):
        '''Test `stable_checkparams` low-level function'''
        lib = pystable.load_libstable()
        expected_args = (ct.c_double, ct.c_double, ct.c_double, ct.c_double,
                         ct.c_int)
        actual = pystable.c_stable_checkparams(lib)

        self.assertEqual('stable_checkparams', actual.__name__)
        self.assertEqual(expected_args, actual.argtypes)
        self.assertEqual(ct.c_int, actual.restype)

    def test_stable_checkparams_err(self):
        pass

    def test_create(self):
        '''Test `create` wrapper'''
        expected = {
                'alpha': 1.3278285879842862,
                'beta': 0.0816835526225623,
                'sigma': 0.0006409442772706,
                'mu_0': -0.00011779403879886721,
                'mu_1': -2.52748167384e-05
                }
        params = self.get_fit()
        actual = pystable.create(params)
        self.assertEqual(expected['alpha'], actual.contents.alpha)
        self.assertEqual(expected['beta'], actual.contents.beta)
        self.assertEqual(expected['sigma'], actual.contents.sigma)
        self.assertEqual(expected['mu_0'], actual.contents.mu_0)
        self.assertEqual(expected['mu_1'], actual.contents.mu_1)

    def test_stable_create(self):
        '''Test `stable_cdf` high-level function'''
        lib = pystable.load_libstable()
        params = self.get_fit()
        expected = {
                'alpha': 1.3278285879842862,
                'beta': 0.0816835526225623,
                'sigma': 0.0006409442772706,
                'mu_0': -0.00011779403879886721,
                'mu_1': -2.52748167384e-05
                }
        actual = pystable.stable_create(lib, params)

        self.assertEqual(expected['alpha'], actual.contents.alpha)
        self.assertEqual(expected['beta'], actual.contents.beta)
        self.assertEqual(expected['sigma'], actual.contents.sigma)
        self.assertEqual(expected['mu_0'], actual.contents.mu_0)
        self.assertEqual(expected['mu_1'], actual.contents.mu_1)

    def test_c_stable_create(self):
        '''Test `stable_cdf` low-level function'''
        lib = pystable.load_libstable()
        expected_args = (ct.c_double, ct.c_double, ct.c_double, ct.c_double,
                         ct.c_int)
        expected_res = ct.POINTER(pystable.STABLE_DIST)
        actual = pystable.c_stable_create(lib)

        self.assertEqual('stable_create', actual.__name__)
        self.assertEqual(expected_args, actual.argtypes)
        self.assertEqual(expected_res, actual.restype)

    @unittest.skip(reason='failing')
    def test_stable_fit(self):
        '''Test `stable_fit` high-level function'''
        lib = pystable.load_libstable()
        fit = self.get_fit()
        expected = [fit['alpha'], fit['beta'], fit['sigma'], 0, fit['mu']]

        init_fit = {'alpha': 2, 'beta': 0, 'sigma': 1, 'mu': 0,
                    'parameterization': 1}
        dist = pystable.stable_create(lib, init_fit)

        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, 'helpers')
        base = os.path.join(base, 'data.csv')
        data = pd.read_csv(base)['value'].to_numpy().tolist()

        fit_params = {'dist': dist, 'data': data, 'length': len(data)}
        status = pystable.stable_fit(lib, fit_params)
        assert status == 0  # 0 == finished
        actual = [dist.contents.alpha, dist.contents.beta,
                  dist.contents.sigma, dist.contents.mu_0, dist.contents.mu_1]
        np.testing.assert_allclose(expected, actual, rtol=1e-05)

    def test_c_stable_fit(self):
        '''Test `stable_fit` low-level function'''
        lib = pystable.load_libstable()
        actual = pystable.c_stable_fit(lib)
        self.assertEqual('stable_fit', actual.__name__)

    def test_stable_cdf(self):
        '''Test `stable_cdf` high-level function'''
        lib = pystable.load_libstable()

        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, 'helpers/fit.csv')
        fit = pd.read_csv(base).to_dict(orient='records')[0]
        dist = pystable.stable_create(lib, fit)

        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, 'helpers')
        base = os.path.join(base, 'cdfs.csv')
        cdfs = pd.read_csv(base)
        expected = cdfs['value'].tolist()

        x = cdfs['x'].to_numpy().tolist()
        Nx = len(x)
        cdf_params = {'dist': dist, 'x': x, 'Nx': Nx}

        actual = pystable.stable_cdf(lib, cdf_params)
        np.testing.assert_allclose(expected, actual, rtol=1e-08)

    def test_stable_cdf_point(self):
        '''Test `stable_cdf_point` high-level function'''
        lib = pystable.load_libstable()

        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, 'helpers/fit.csv')
        fit = pd.read_csv(base).to_dict(orient='records')[0]
        dist = pystable.stable_create(lib, fit)
        params = {'dist': dist, 'x': -0.009700000000000002}
        actual = pystable.stable_cdf_point(lib, params)

        expected = 0.006362143180580383
        self.assertEqual(expected, actual)

    def test_c_stable_cdf_point(self):
        '''Test `stable_cdf_point` low-level function'''
        lib = pystable.load_libstable()
        actual = pystable.c_stable_cdf_point(lib)
        self.assertEqual('stable_cdf_point', actual.__name__)

    def test_stable_pdf(self):
        '''Test `stable_pdf` high-level function'''
        lib = pystable.load_libstable()

        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, 'helpers')
        base = os.path.join(base, 'pdfs.csv')
        pdfs = pd.read_csv(base)

        expected = pdfs['value'].tolist()

        x = pdfs['x'].tolist()
        dist = pystable.stable_create(lib, self.get_fit())
        params = {'dist': dist, 'x': x, 'Nx': len(x)}
        actual = pystable.stable_pdf(lib, params)
        np.testing.assert_allclose(expected, actual, rtol=1e-06)

    def test_c_stable_pdf(self):
        '''Test `stable_pdf` low-level function'''
        lib = pystable.load_libstable()
        actual = pystable.c_stable_pdf(lib)
        self.assertEqual('stable_pdf', actual.__name__)

    def test_stable_q(self):
        '''Test `stable_q` high-level function'''
        lib = pystable.load_libstable()

        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.join(base, 'helpers')
        base = os.path.join(base, 'quantiles.csv')
        quantiles = pd.read_csv(base)

        expected = quantiles['value'].tolist()

        q = quantiles['q'].tolist()
        dist = pystable.stable_create(lib, self.get_fit())
        params = {'dist': dist, 'q': q, 'Nq': len(q)}
        print(params)
        actual = pystable.stable_q(lib, params)
        np.testing.assert_allclose(expected, actual, rtol=1e-05)

    def test_c_stable_q(self):
        '''Test `stable_q` low-level function'''
        lib = pystable.load_libstable()
        actual = pystable.c_stable_q(lib)
        self.assertEqual('stable_q', actual.__name__)

    @unittest.skip(reason='Need test vectors')
    def test_stable_rnd(self):
        '''Test `stable_rnd` high-level function'''
        pass

    def test_c_stable_rnd(self):
        '''Test `stable_rnd` low-level function'''
        lib = pystable.load_libstable()
        actual = pystable.c_stable_rnd(lib)
        self.assertEqual('stable_rnd', actual.__name__)
