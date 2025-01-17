from setuptools import setup
from Cython.Build import cythonize
setup(
name=('test_IV_Sweep'),
ext_modules=cythonize('test_IV_Sweep.py')
)
# python pyd_setup.py build_ext --inplace