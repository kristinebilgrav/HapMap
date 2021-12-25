from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize(
           "onenewgraph_2.pyx",               
           language="c++",
      ))
