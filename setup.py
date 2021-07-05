from distutils.core import setup, Extension

libstable_module = Extension('libstable',
                             include_dirs=["./libstable/stable/src/"],
                             library_dirs=["./libstable/stable/libs/"],
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

setup(name='PackageName',
      version='1.0',
      description='This is a demo package',
      author='',
      author_email='',
      url='',
      long_description='''This is really just a demo package.''',
      ext_modules=[libstable_module])
