# pystable

Python wrapper for the [`libstable`](https://www.jstatsoft.org/article/view/v078i01) C library.

## Example

To fit with ML estimation:

```python
import pystable

alpha, beta, loc, scale = pystable.fit(data)
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
