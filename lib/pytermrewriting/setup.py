from setuptools import setup

import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

termrewritingpath = os.path.abspath("../termrewriting")
termrewritinginc = termrewritingpath + "/inc"

ext_modules = [Extension("pytermrewriting",
                     ["./pytermrewriting/PyVariableName.pyx,./pytermrewriting/VariableName.pxd"],
                     language='c++',
                     include_dirs=[termrewritinginc],
                     library_dirs=[termrewritingpath],
                     libraries=["termrewriting"]
                     )]

setup(
    name='pytermrewriting',
    version='0.0.1',
    packages=[],
    url='',
    license='',
    author='andrewlawrence',
    author_email='andrew.lawrence@siemens.com',
    description='',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)
