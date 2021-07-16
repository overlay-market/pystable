# pystable

Python wrapper for the [`libstable`](https://www.jstatsoft.org/article/view/v078i01) C library.

## Example

To fit with ML estimation:

```python
import pystable

alpha, beta, loc, scale = pystable.fit(data)
```

## Build `libstable`
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

## Build `libstable`
```
$ cd libstable
$ make
```

or

```
$ poetry shell
$ poetry build
```



## TODO
- [ ] typings
- [ ] tests
- [ ] handle errors
  - [ ] handle NULL pointer errors
  - [ ] handle `err`
- [ ] create lib structure
- [x] create example file utilizing pystable lib
- [x] `import ctypes as ct`
- [ ] Main functions:
  - [ ] `stable_pdf`: `./libstable/stable/src/stable.h#L256`
  - [ ] `stable_cdf`: `./libstable/stable/src/stable.h#L287`
  - [ ] `stable_q`: `./libstable/stable/src/stable.h#L301`
  - [ ] `stable_rnd`: `./libstable/stable/src/stable.h#L446`
  - [ ] `stable_fit` we'll probably have to do something similar to the matlab front end code where we use multiple fitting fns of theres
