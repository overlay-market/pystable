import os
import pandas as pd
import sys
sys.path.append('/home/rrybarczyk/Dev/pystable')
import pystable  # noqa: E402


def read_helpers(file_name: str):
    path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.abspath(os.path.join(path, os.pardir))
    path = os.path.abspath(os.path.join(path, 'tests/helpers'))
    path = os.path.abspath(os.path.join(path, file_name))

    return pd.read_csv(path)


def get_fn_params(fn_name: str, dist):
    df_params = read_helpers('{}.csv'.format(fn_name))
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


def get_quantiles_params(dist):
    df_params = read_helpers('quantiles.csv')
    q = []
    for i in df_params['q']:
        q.append(i)
    Nq = len(q)
    fn_data = [0] * Nq
    return {
            'dist': dist,
            'q': q,
            'Nq': Nq,
            'fn': fn_data,
        }


def run() -> None:
    lib = pystable.load_libstable()
    dist_params = {
            'alpha': 1.3278285879842862,
            'beta': 0.0816835526225623,
            'mu': -0.0000252748167384907,  # loc
            'sigma': 0.0006409442772706084,  # scale
            'parameterization': 1,
        }
    # Check `dist_params` validity
    check = pystable.stable_checkparams(lib, dist_params)
    print('stable_checkparams (0 means OK): ', check)
    print()

    # Call `create_stable` input args to create pointer to `StableDist` struct
    dist = pystable.stable_create(lib, dist_params)
    print('DIST', type(dist))
    dist_result = {
              'alpha': dist.contents.alpha,
              'beta': dist.contents.beta,
              'sigma': dist.contents.sigma,
              'mu_0': dist.contents.mu_0,
              'mu_1': dist.contents.mu_1,
            }
    print('stable_create dist result: ', dist_result)
    print()

    # `stable_cdf_point`
    stable_cdf_point_params = {'dist': dist, 'x': -0.009700000000000002}
    ret = pystable.stable_cdf_point(lib, stable_cdf_point_params)
    print('stable_cdf_point result: ', ret)
    print()

    # `stable_cdf`
    cdf_params = get_fn_params('cdf', dist)
    cdf = pystable.stable_cdf(lib, cdf_params)
    print('stable_cdf result: ', cdf)
    print()

    # `stable_fit`, TODO

    # `stable_pdf`
    pdf_params = get_fn_params('pdf', dist)
    pdf = pystable.stable_pdf(lib, pdf_params)
    print('stable_pdf result: ', pdf)
    print()

    # `stable_q`
    q_params = get_quantiles_params(dist)
    q = pystable.stable_q(lib, q_params)
    print('stable_q result: ', q)
    print()


if __name__ == "__main__":
    run()
