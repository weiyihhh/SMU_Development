import distutils.core
from Cython.Build import cythonize
from Cython.Distutils import build_ext

a = cythonize("smu_measure.py")[0]
distutils.core.setup(
    name = 'smu_measure',
    version = '1.0',
    ext_modules = [a],
    author = '',
)
#python PYD_make.py build_ext --inplace