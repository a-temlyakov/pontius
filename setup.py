from distutils.core import setup

setup(
    name='pontius',
    version='0.0.1',
    author='Andrew Temlyakov',
    author_email='temlyaka@gmail.com',
    packages=['pontius'],
    scripts=['bin/pontius'],
    license='LICENSE.txt',
    description='CLI for managing and deleting duplicate files.',
    long_description=open('README.md').read(),
    )
