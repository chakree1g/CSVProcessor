'''
Basic setup file with Readme and License info.
Austomatically packages all modules!
'''

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

setup(
    name='wpe_merge',
    version='0.1.1',
    description='Simple CSV processor',
    long_description=readme,
    author='Chakradhar Kondapalli',
    author_email='chakree1g@gmail.com',
    data_files = [("", ["LICENSE"])],
    packages=find_packages(),
    test_suite = 'nose.collector',
    tests_require = ['nose', 'path.py'],
    install_requires=[
       'pandas',
       'requests'
   ],
    entry_points={
    'console_scripts': [ 
        'wpe_merge = csvprocessor.csvprocessor:main' 
    ] 
    }
)

