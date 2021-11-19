import setuptools 

setuptools.setup(
    name='nbastats',
    version='1',
    author='David Saunders',
    author_email='d.saunders@yale.edu',
    description='Predicting NBA player statlines',
    packages=['nbastats', 'nbastats/processing', 'nbastats/modelling', 'nbastats/plotting'],
    long_description=readme(),
    python_requires='>=3.7',
    url='https://github.com/NbaStats',
    install_requires=['numpy>=2','scipy>=1','matplotlib>=3']
)