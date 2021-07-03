import os
import pytest
import pandas as pd
import numpy as np
import pystable


@pytest.fixture
def stables() -> pd.DataFrame:
    """
    Fixture to get stable distribution examples
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'stable')
    # TODO: should have csv w rows as (a, b, loc, scale, cdf_values, pdf_values, quantile_values)
    base = os.path.join(base, 'stables.csv')
    return pd.read_csv(base)


@pytest.fixture
def dataset() -> (pd.DataFrame, pd.DataFrame):
    """
    Fixture to get dataset and associated fit
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'data')
    base = os.path.join(base, 'data.csv')  # TODO:

    data = pd.read_csv(os.path.join(base, 'data.csv'))
    fit = pd.read_csv(os.path.join(base, 'fit.csv'))
    return data, fit


def test_cdf(stables):
    """
    Tests cdf values for stable examples
    """
    pass


def test_pdf(stables):
    """
    Tests pdf values for stable examples
    """
    pass


def test_quantile(stables):
    """
    Tests quantile values for stable examples
    """
    pass


def test_fit(dataset):
    """
    Tests stable param estimation for data
    """
    data, fit = dataset
    params = pystable.fit(data)
    assert np.testing.assert_allclose(fit, params, rtol=1e-08)
