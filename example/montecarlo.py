import pandas as pd
import numpy as np
import time
import pystable


PERIOD = 10*60  # 10 m
N = int(86400*90/PERIOD)  # 90d - number of 10 min periods into future
SIMS = 100
P0 = 0.00823305  # initial price
FIT = {
    "alpha": 1.4430192097069168,
    "beta": 0.042938293127910906,
    "sigma": 0.004747879945834797,
    "mu": -0.0004197632840157609,
    "parameterization": 1,
}  # 1h fit
FIT_RESCALE = 1/6.  # scale down to 10m


def rescale_dist(dist: pystable.STABLE_DIST,
                 rescale: float) -> pystable.STABLE_DIST:
    alpha = dist.contents.alpha
    beta = dist.contents.beta
    sigma = dist.contents.sigma * (rescale) ** (1/alpha)
    mu_1 = dist.contents.mu_1 * rescale
    return pystable.create(alpha, beta, sigma, mu_1, 1)


def generate_ts(period: float, n: int) -> np.ndarray:
    return np.arange(0, (n+1)*period, period)


def generate_rs(dist: pystable.STABLE_DIST, n: int) -> np.ndarray:
    rs = np.asarray([0] + pystable.rnd(dist, n))  # 0 added for e^0 * p0
    return rs


def generate_sims(dist: pystable.STABLE_DIST,
                  period: int, n: int, sims: int, p0: float) -> pd.DataFrame:
    p_data = []
    for i in range(sims):
        rs = generate_rs(dist, n)
        print(f'rs-{i}', rs)
        dp = np.cumsum(rs)
        dp = np.exp(dp)
        p = P0 * dp
        p_data.append(p)

    ts = generate_ts(period, n)
    print(f'ts-{i}', ts)
    df = pd.DataFrame(data=[ts, *p_data]).T

    columns = ['timestamp'] + [f"sim-{i}" for i in range(sims)]
    df.columns = columns
    return df


def run() -> None:
    # Load libstable CDLL
    alpha = FIT['alpha']
    beta = FIT['beta']
    sigma = FIT['sigma']
    mu = FIT['mu']
    parameterization = FIT['parameterization']

    # Check `fit` validity, returns 0 on success
    check = pystable.checkparams(alpha, beta, sigma, mu, parameterization)
    assert check == 0

    # Call `create_stable` input args to create pointer to `StableDist` struct
    dist = pystable.create(alpha, beta, sigma, mu, parameterization)
    dist = rescale_dist(dist, FIT_RESCALE)
    print('DIST', type(dist))
    dist_result = {
              'alpha': dist.contents.alpha,
              'beta': dist.contents.beta,
              'sigma': dist.contents.sigma,
              'mu_0': dist.contents.mu_0,
              'mu_1': dist.contents.mu_1,
            }
    print('stable_create dist result: {}\n'.format(dist_result))
    df = generate_sims(dist, PERIOD, N, SIMS, P0)
    print('df', df)
    df.to_csv(f"mc-{time.time()}.csv")


if __name__ == "__main__":
    run()
