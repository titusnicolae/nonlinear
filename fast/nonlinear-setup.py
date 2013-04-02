from distutils.core import setup, Extension

setup(name="nonlinear", version="1.0",
      ext_modules=[Extension("nonlinear", ["nonlinearmodule.c"])])
