#!/usr/bin/env python

"""The setup script."""
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [ ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Julian Lehrer",
    author_email='jmlehrer@ucsc.edu',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
#   description="Convert sql queries to pandas",
#
#    entry_points={
#        'console_scripts': [
#            'sql_to_pandas=sql_to_pandas.cli:main',
#        ],
#    },
#
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sql_to_pandas',
    name='sql_to_pandas',
    packages=find_packages(include=['sql_to_pandas', 'sql_to_pandas.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jlehrer1/sql_to_pandas',
    version='0.1.0',
