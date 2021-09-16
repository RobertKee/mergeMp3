"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='merge_mp3',
    version='1.0.0',
    description='merge mp3 files with a single command',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/roberthayeskee/mergemp3',
    author='Robert Kee',
    author_email='robert@roberthayeskee.com',
    keywords='mp3, files, media',
    package_dir={'': 'src'}, 
    packages=find_packages(where='src'), 
    python_requires='>=3.6, <4',
    install_requires=['peppercorn,subprocess,os,sys,mutagen'],
    entry_points={  
        'console_scripts': [
            'merge-mp3=merge:merge_mp3',
        ],
    },
)
