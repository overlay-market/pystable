import os
import pytest
import typing as tp
import pandas as pd
import numpy as np
import pystable


@pytest.fixture
def fit() -> tp.List[float]:
    """
    Fixture to get stable distribution example params
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'fit.csv')
    return pd.read_csv(base).to_numpy().tolist()


@pytest.fixture
def data() -> tp.List[float]:
    """
    Fixture to get dataset and associated fit
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'data.csv')
    return pd.read_csv(base).to_numpy().tolist()


@pytest.fixture
def cdfs() -> pd.DataFrame:
    """
    Fixture to get dataset and associated fit
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'cdfs.csv')
    return pd.read_csv(base)


@pytest.fixture
def pdfs() -> pd.DataFrame:
    """
    Fixture to get dataset and associated fit
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'pdfs.csv')
    return pd.read_csv(base)


@pytest.fixture
def quantiles() -> pd.DataFrame:
    """
    Fixture to get dataset and associated fit
    """
    base = os.path.dirname(os.path.abspath(__file__))
    base = os.path.join(base, 'helpers')
    base = os.path.join(base, 'quantiles.csv')
    return pd.read_csv(base)


def test_cdf(fit, cdfs):
    """
    Tests cdf values for stable examples
    """
    pass


def test_pdf():
    """
    Tests pdf values for stable examples
    """
    pass


def test_quantile():
    """
    Tests quantile values for stable examples
    """
    pass


def test_fit(fit, data):
    """
    Tests stable param estimation for data
    """
    expected = fit
    actual = pystable.fit(data)
    assert np.testing.assert_allclose(expected, actual, rtol=1e-08)
