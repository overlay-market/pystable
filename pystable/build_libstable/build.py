from cffi import FFI

ffibuilder = FFI()

ffibuilder.set_source(
    include_dirs=[],
    library_dirs=[],
    libraries=[],
)

ffibuilder.compile(verbose=True)
