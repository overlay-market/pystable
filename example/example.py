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
    lib = pystable.load_libstable()
    fit = read_helpers('fit.csv')

    # Check `fit` validity, returns 0 on success
    check = pystable.stable_checkparams(lib, fit)
    assert check == 0

    # Call `create_stable` input args to create pointer to `StableDist` struct
    dist = pystable.stable_create(lib, fit)
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
    stable_cdf_point_params = {'dist': dist, 'x': -0.009700000000000002}
    ret = pystable.stable_cdf_point(lib, stable_cdf_point_params)
    print('stable_cdf_point result: {}\n'.format(ret))

    df_params = read_helpers('cdfs.csv')
    x = []
    for i in df_params['x']:
        x.append(i)
    Nx = len(x)
    cdf_params = {'dist': dist, 'x': x, 'Nx': Nx}

    # Call `stable_cdf`
    cdf = pystable.stable_cdf(lib, cdf_params)
    print('stable_cdf result: ', cdf)


if __name__ == "__main__":
    run()
