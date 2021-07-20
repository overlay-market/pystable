# pystable

Python wrapper for the [`libstable`](https://www.jstatsoft.org/article/view/v078i01) C library.

## Example

To fit with ML estimation:

```python
import pystable

init_fit = {'alpha': 2, 'beta': 0, 'sigma': 1, 'mu': 0,
            'parameterization': 1}
dist = pystable.create(init_fit['alpha'], init_fit['beta'],
                       init_fit['sigma'], init_fit['mu'],
                       init_fit['parameterization'])

pystable.fit(dist, data, len(data))
fit_params = [dist.contents.alpha, dist.contents.beta,
              dist.contents.sigma, dist.contents.mu_0, dist.contents.mu_1]
```

## Setup
### Dependencies
Install the GNU Scientific Library (GSL).

Arch Linux:
```
$ yay gsl
```

Mac:
```
$ brew install gsl
```

Ubuntu:
```
$ sudo apt install gsl-bin libgsl0-dev
```

### Build `libstable`
```
$ cd libstable
$ make
```

or

```
$ poetry build
```

## TODO
- [x] `import ctypes as ct`
- [x] create lib structure
- [x] create example file utilizing pystable lib
- [ ] typings
- [ ] handle errors
  - [ ] handle NULL pointer errors
  - [ ] handle `err`
- [x] `stable_checkparams`
  - [x] impl
  - [x] test
  - [x] example
  - [ ] handle error
  - [ ] test error
- [x] `stable_create`
  - [x] impl
  - [x] test
  - [x] example
- [x] `stable_cdf`
  - [x] impl
  - [x] test
  - [x] example
- [x] `stable_pdf`
  - [x] impl
  - [x] test
  - [x] example
- [x] `stable_fit`
  - [x] impl
  - [ ] test
  - [ ] example
- [ ] `stable_q`
  - [x] impl
  - [x] test
  - [ ] example
- [ ] `stable_rnd`
  - [x] impl
  - [ ] test
  - [ ] example
