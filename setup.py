import os
import pathlib
import shutil
import subprocess
import sys

from distutils.command.build_ext import build_ext
from distutils.core import setup, Extension


libstable_module = Extension('libstable',
                             libraries=["blas", "gsl", "m", "gslcblas"],
                             sources=[
                                "./libstable/stable/src/mcculloch.c",
                                "./libstable/stable/src/methods.c",
                                "./libstable/stable/src/stable_cdf.c",
                                "./libstable/stable/src/stable_common.c",
                                "./libstable/stable/src/stable_dist.c",
                                "./libstable/stable/src/stable_fit.c",
                                "./libstable/stable/src/stable_integration.c",
                                "./libstable/stable/src/stable_koutrouvelis.c",
                                "./libstable/stable/src/stable_pdf.c",
                                "./libstable/stable/src/stable_q.c",
                                "./libstable/stable/src/stable_rnd.c"])


# SEE: https://github.com/python-poetry/poetry/issues/11
class ExtensionBuild(build_ext):
    def run(self):
        # Make libstable
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.abspath(os.path.join(path, 'libstable'))
        proc = subprocess.run(['make'], cwd=path)
        if proc.returncode != 0:
            print('Error building libstable')
            sys.exit(-1)
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
                "./pystable/_extensions",  # TODO: remove hard code
                ext.name+file_extension
            )
            shutil.copyfile(output, dest)
            mode = os.stat(dest).st_mode
            mode |= (mode & 0o444) >> 2
            os.chmod(dest, mode)


setup(ext_modules=[libstable_module], cmdclass=dict(build_ext=ExtensionBuild))
