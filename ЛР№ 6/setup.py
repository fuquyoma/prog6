from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("ferma_fact.pyx", annotate=True, language_level=3),
)

setup(
    ext_modules=cythonize("ferma_factGIL.pyx",annotate=True, language_level="3", language="c")
) 