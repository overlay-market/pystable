import os
import pytest
import ctypes as ct
import typing as tp
import pandas as pd
import numpy as np
import time

import pystable


def create_stable(clib: ct.CDLL, params: tp.Dict[str, float]):
    return pystable.stable_create(clib, params)


@pytest.fixture
def lib() -> ct.CDLL:
    """
    Fixture to get C library
    """
    return pystable.load_libstable()


@pytest.fixture
def data() -> tp.List[float]:
    """
    Fixture to get example dataset
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'data.csv')
    return pd.read_csv(base)['value'].to_numpy().tolist()


@pytest.fixture
def fit() -> tp.Dict[str, float]:
    """
    Fixture to get stable distribution example params.
    Should fit the example dataset.
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'fit.csv')
    return pd.read_csv(base).to_dict(orient='records')[0]


@pytest.fixture
def cdfs() -> pd.DataFrame:
    """
    Fixture to get generated cdf values from example stable distribution
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'cdfs.csv')
    return pd.read_csv(base)


@pytest.fixture
def pdfs() -> pd.DataFrame:
    """
    Fixture to get generated pdf values from example stable distribution
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'pdfs.csv')
    return pd.read_csv(base)


@pytest.fixture
def quantiles() -> pd.DataFrame:
    """
    Fixture to get generated cdf^{-1} values from example stable distribution
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'quantiles.csv')
    return pd.read_csv(base)


# Low level wrapper tests

def test_stable_create(lib, fit):
    """
    Tests creation of stable distribution
    """
    dist = create_stable(lib, fit)
    # TODO: assert type(dist) == pystable.STABLE_DIST ... diff bw <class 'pystable.pystable.LP_STABLE_DIST'> == <class 'pystable.pystable.STABLE_DIST'>?

    assert fit['alpha'] == dist.contents.alpha
    assert fit['beta'] == dist.contents.beta
    assert fit['sigma'] == dist.contents.sigma

    if fit['parameterization'] == 1:
        assert fit['mu'] == dist.contents.mu_1
    else:
        assert fit['mu'] == dist.contents.mu_0


def test_stable_cdf(lib, fit, cdfs):
    """
    Tests cdf values for stable example
    """
    expected = cdfs['value'].tolist()

    dist = create_stable(lib, fit)
    x = cdfs['x'].to_numpy().tolist()
    Nx = len(x)
    cdf = [0] * Nx
    cdf_params = {
        'dist': dist,
        'x': x,
        'Nx': Nx,
        'cdf': cdf
    }

    actual = pystable.stable_cdf(lib, cdf_params)
    np.testing.assert_allclose(expected, actual, rtol=1e-08)


def test_stable_pdf(lib, fit, pdfs):
    """
    Tests cdf values for stable example
    """
    expected = pdfs['value'].tolist()

    dist = create_stable(lib, fit)
    x = pdfs['x'].to_numpy().tolist()
    Nx = len(x)
    pdf = [0] * Nx
    pdf_params = {
        'dist': dist,
        'x': x,
        'Nx': Nx,
        'pdf': pdf
    }

    actual = pystable.stable_pdf(lib, pdf_params)
    np.testing.assert_allclose(expected, actual, rtol=1e-08)


def test_stable_fit(lib, fit, data):
    """
    Tests fit values for stable example
    """
    expected = [fit['alpha'], fit['beta'], fit['sigma'], 0, fit['mu']]

    init_fit = {
        'alpha': 2,
        'beta': 0,
        'sigma': 1,
        'mu': 0,
        'parameterization': 1
    }
    dist = create_stable(lib, init_fit)

    length = len(data)
    fit_params = {
        'dist': dist,
        'data': data,
        'length': length,
    }

    # time it ...
    start = time.time()
    status = pystable.stable_fit(lib, fit_params)
    end = time.time()
    print('start', start)
    print('end', end)
    print('execution time', end - start)

    actual = [dist.contents.alpha, dist.contents.beta,
              dist.contents.sigma, dist.contents.mu_0, dist.contents.mu_1]

    np.testing.assert_allclose(expected, actual, rtol=1e-08)

    # TODO: assert status > 0 ?


# Public API tests

def test_cdf(fit, cdfs):
    """
    Tests cdf values for stable example
    """
    expected = cdfs['value'].tolist()
    x = cdfs['x'].to_numpy().tolist()
    actual = pystable.cdf(x, *fit)
    np.testing.assert_allclose(expected, actual, rtol=1e-08)


def test_pdf(fit, pdfs):
    """
    Tests pdf values for stable example
    """
    expected = pdfs['value'].tolist()
    x = pdfs['x'].to_numpy().tolist()
    actual = pystable.pdf(x, *fit)
    np.testing.assert_allclose(expected, actual, rtol=1e-08)


def test_quantile(fit, quantiles):
    """
    Tests quantile values for stable example
    """
    expected = quantiles['value'].tolist()
    q = quantiles['q'].to_numpy().tolist()
    actual = pystable.q(q, *fit)
    np.testing.assert_allclose(expected, actual, rtol=1e-08)


def test_fit(fit, data):
    """
    Tests stable param estimation for dataset
    """
    expected = fit
    actual = pystable.fit(data)
    np.testing.assert_allclose(expected, actual, rtol=1e-08)
