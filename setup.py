import os
import pathlib
import shutil
import setuptools

from distutils.command.build_ext import build_ext
from distutils.core import Extension

base = os.path.dirname(os.path.abspath(__file__))

libstable_srcs = [
    os.path.join(base, "pystable/libstable/stable/src/mcculloch.c"),
    os.path.join(base, "pystable/libstable/stable/src/methods.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_cdf.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_common.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_dist.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_fit.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_integration.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_koutrouvelis.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_pdf.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_q.c"),
    os.path.join(base, "pystable/libstable/stable/src/stable_rnd.c"),
]
libstable_module = Extension('libstable',
                             libraries=["blas", "gsl", "m", "gslcblas"],
                             sources=libstable_srcs)


# SEE: https://github.com/python-poetry/poetry/issues/11
class ExtensionBuild(build_ext):
    def run(self):
        build_ext.run(self)

        # Copy built extensions back to project
        self.check_extensions_list(self.extensions)
        for ext in self.extensions:
            output = self.get_ext_fullpath(ext.name)
            if not os.path.exists(output):
                continue

            relative_extension = os.path.relpath(output, self.build_lib)
            file_extension = pathlib.Path(relative_extension).suffix
            dest = os.path.join(
                base,
                "pystable/_extensions",
                ext.name+file_extension
            )
            shutil.copyfile(output, dest)
            mode = os.stat(dest).st_mode
            mode |= (mode & 0o444) >> 2
            os.chmod(dest, mode)


setuptools.setup(ext_modules=[libstable_module],
                 cmdclass=dict(build_ext=ExtensionBuild))
