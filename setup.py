"""
Dalmatiner Python Client
"""

import os
import re
from setuptools import find_packages, setup


def fread(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    VERSIONFILE = "ddb-python/_version.py"
    verstrline = fread(VERSIONFILE).strip()
    vsre = r"^__version__ = ['\"]([^'\"]*)['\"]"
    mo = re.search(vsre, verstrline, re.M)
    if mo:
        VERSION = mo.group(1)
    else:
        raise RuntimeError("Unable to find version string in %s." %
                           (VERSIONFILE, ))
    return VERSION


dependencies = ['nose']

setup(name='ddb-python',
      version=get_version(),
      url='https://github.com/dataloop/dalmatiner-python-client',
      download_url=
      "https://github.com/dataloop/dalmatiner-python-client/tarball/v" +
      get_version(),
      license="Apache License, Version 2.0",
      author='Steven Acreman',
      author_email='steven.acreman@dataloop.io',
      description='Dalmatiner Python Client',
      long_description=fread('README.rst'),
      keywords="dataloop dalmatiner",
      packages=find_packages(exclude=['tests']),
      include_package_data=True,
      zip_safe=False,
      platforms='any',
      install_requires=dependencies,
      entry_points={},
      classifiers=[
          "Intended Audience :: Developers",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: Apache Software License",
      ])
