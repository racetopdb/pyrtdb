import os
from setuptools import setup
import setuptools

about = {}
LIB_NAME = "pyrtdb"
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(PROJECT_DIR, LIB_NAME, '__version__.py')) as f:
    exec(f.read(), about)

with open('README.md', mode='r', encoding='utf-8') as f:
    readme = f.read()


setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__description__'],
    long_description=readme,
    long_description_content_type='text/markdown',
    author=about['__author__'],
    author_email=about['__author_email__'],
    url=about['__url__'],
    package_dir={'pyrtdb': 'pyrtdb'},
    data_files=[('pyrtdb/dll/linux', ['pyrtdb/dll/linux/libtsdb.so']), 
    ('pyrtdb/dll/windows/', ['pyrtdb/dll/windows/win32/tsdb.dll', 'pyrtdb/dll/windows/x64/tsdb.dll'])],
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    license=about['__license__'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],

)
