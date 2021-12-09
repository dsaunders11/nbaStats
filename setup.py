import setuptools 

setuptools.setup(
    name='nbastats',
    version='1',
    author='David Saunders',
    author_email='d.saunders@yale.edu',
    description='Predicting NBA player statlines',
    packages=['nbaStats'],
    python_requires='>=3.7',
    url='https://github.com/NbaStats',
    install_requires=['numpy','pandas','matplotlib', 'requests', 'datetime', 'time']
)