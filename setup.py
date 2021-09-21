from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
exec(open("src/merge/version.py").read())

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='merge_mp3',
    version=__version__,
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
    install_requires=['peppercorn','mutagen','Path'],
    entry_points={  
        'console_scripts': [
            'merge-mp3=merge.merge:merge_mp3',
        ],
    },
)
