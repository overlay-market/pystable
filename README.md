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

## Build `libstable`
```
$ cd libstable
$ make
```


