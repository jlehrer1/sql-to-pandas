import pathlib
from distutils.core import setup
import setuptools
from setuptools import find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='sqltopandas',         # How you named your package folder (MyLib)
    packages=find_packages(exclude=("tests",)),  
    version='0.01',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    description='Use SQL expressions to query Pandas DataFrames',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Julian Lehrer',                   # Type in your name
    author_email='julianmlehrer@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/jlehrer1/sql-to-pandas',
    # Keywords that define your package best
    keywords=['SQL', 'PYTHON', 'DATA SCIENCE', 'PANDAS', 'DATAFRAME'],
    install_requires=[            # I get to this in a second
        'numpy',
        'pandas',
        'numpy',
        'sqlparse',
        'pytest'
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        'Programming Language :: Python :: 3.8',
    ],
    include_package_data=True,
)
