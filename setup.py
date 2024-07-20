# Author: Kengo Sugahara <ksugahar@gmail.com>
# Copyright (c) 2024 Kengo Sugahara
# License: BSD 3 clause

from setuptools import setup
import cubit_mesh_export

DESCRIPTION = "Cubit_Mesh_Export: Cubit mesh export to Gmsh format"
NAME = 'cubit_mesh_export'
AUTHOR = 'Kengo Sugahara'
AUTHOR_EMAIL = 'ksugahar@gmail.com'
URL = 'https://github.com/ksugahar/Coreform_Cubit_Python_API'
LICENSE = 'BSD 3-Clause'
DOWNLOAD_URL = 'https://github.com/ksugahar/Coreform_Cubit_Python_API'
VERSION =  '0.2.0'
PYTHON_REQUIRES = ">=3.7"

INSTALL_REQUIRES = [
	'numpy >=1.20.3',
	'scipy>=1.6.3',
]

EXTRAS_REQUIRE = {
}

PACKAGES = [
	'.'
]

CLASSIFIERS = [
	'Intended Audience :: Science/Research',
	'License :: OSI Approved :: BSD License',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.6',
	'Programming Language :: Python :: 3.7',
	'Programming Language :: Python :: 3.8',
	'Programming Language :: Python :: 3.9',
	'Programming Language :: Python :: 3 :: Only',
	'Topic :: Scientific/Engineering',
	'Topic :: Scientific/Engineering :: Artificial Intelligence',
]

setup(name=NAME,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      maintainer=AUTHOR,
      maintainer_email=AUTHOR_EMAIL,
      description=DESCRIPTION,
      long_description='',
      license=LICENSE,
      url=URL,
      version=VERSION,
      download_url=DOWNLOAD_URL,
      python_requires=PYTHON_REQUIRES,
      install_requires=INSTALL_REQUIRES,
      extras_require=EXTRAS_REQUIRE,
      packages=PACKAGES,
      classifiers=CLASSIFIERS,
    )
