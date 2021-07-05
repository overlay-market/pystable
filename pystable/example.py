import pystable
import utils


def run():
    lib = pystable.load_libstable()
    # `create_stable` input args to create pointer to `StableDist` struct
    dist_params = {
            'alpha': 1.3278285879842862,
            'beta': 0.0816835526225623,
            'mu': -0.0000252748167384907,  # loc
            'sigma': 0.0006409442772706084,  # scale
            'parameterization': 1,
        }

    dist = pystable.stable_create(lib, dist_params)
    dist_params = {
              'alpha': dist.contents.alpha,
              'beta': dist.contents.beta,
              'sigma': dist.contents.sigma,
              'mu_0': dist.contents.mu_0,
              'mu_1': dist.contents.mu_1,
            }
    print(dist_params)

    # `stable_cdf_point`
    stable_cdf_point_params = {'dist': dist, 'x': -0.009700000000000002}
    ret = pystable.stable_cdf_point(lib, stable_cdf_point_params)
    print(ret)

    df_params = utils.read_helpers('cdfs.csv')
    x = []
    for i in df_params['x']:
        x.append(i)
    Nx = len(x)
    cdf = [0] * Nx
    cdf_params = {
            'dist': dist,
            'x': x,
            'Nx': Nx,
            'cdf': cdf,
        }

    # `stable_cdf`
    cdf = pystable.stable_cdf(lib, cdf_params)
    print(cdf)
    print(len(cdf))

    pystable.stable_checkparams(lib, 0)


if __name__ == "__main__":
    run()
