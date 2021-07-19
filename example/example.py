import os
import pandas as pd
import pystable


def read_helpers(file_name: str):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    path = os.path.abspath(os.path.join(path, 'tests/helpers'))
    path = os.path.abspath(os.path.join(path, file_name))

    return pd.read_csv(path)


def run() -> None:
    # Load libstable CDLL
    fit = read_helpers('fit.csv')
    alpha = fit['alpha']
    beta = fit['beta']
    sigma = fit['sigma']
    mu = fit['mu']
    parameterization = fit['parameterization']

    # Check `fit` validity, returns 0 on success
    check = pystable.checkparams(alpha, beta, sigma, mu, parameterization)
    assert check == 0

    # Call `create_stable` input args to create pointer to `StableDist` struct
    dist = pystable.create(alpha, beta, sigma, mu, parameterization)
    print('DIST', type(dist))
    dist_result = {
              'alpha': dist.contents.alpha,
              'beta': dist.contents.beta,
              'sigma': dist.contents.sigma,
              'mu_0': dist.contents.mu_0,
              'mu_1': dist.contents.mu_1,
            }
    print('stable_create dist result: {}\n'.format(dist_result))

    # Call `stable_cdf_point`
    x = -0.009700000000000002
    ret = pystable.cdf_point(dist, x)
    print('stable_cdf_point result: {}\n'.format(ret))

    df_params = read_helpers('cdfs.csv')
    x = []
    for i in df_params['x']:
        x.append(i)
    Nx = len(x)

    # Call `stable_cdf`
    cdf = pystable.cdf(dist, x, Nx)
    print('stable_cdf result: ', cdf)


if __name__ == "__main__":
    run()
