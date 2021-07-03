import os
from cffi import FFI

ffibuilder = FFI()
dir_path = os.path.dirname(os.path.realpath(__file__))

libstable_header = []
libstable_header.append(
    os.path.join(dir_path, "libstable_headers/stable.h")
)
for header in libstable_header:
    with open(header, 'rt') as h:
        ffibuilder.cdef(h.read())

ffibuilder.set_source(
    "_libstable",
    """
    #include "stable.h"
    """,
    include_dirs=[""],
    library_dirs=[""],
    libraries=["libstable"]
)

ffibuilder.compile(verbose=True)
