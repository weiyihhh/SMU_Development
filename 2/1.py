from setuptools import setup
from Cython.Build import cythonize
setup(
name=('test_IV_Sweep_Auto'),
ext_modules=cythonize('test_IV_Sweep_Auto.py')
)
# python test1.py build_ext --inplace