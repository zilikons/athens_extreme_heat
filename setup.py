from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='athens_extreme_heat',
      version="0.0.1",
      description="Extreme Heat Vulnerability Analysis for Athens, Greece",
      license="none",
      author="Konstantinos Ziliaskopoulos",
      url="https://github.com/zilikons/athens_extreme_heat",
      install_requires=requirements,
      packages=find_packages(),
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
