
from setuptools import setup, find_namespace_packages

with open('README.md') as f:
    readme = f.read()

setup(
    name="Mazes",
    version='0.0.0',
    description='Mazes for Programmers - Python',
    author='Rob Weddell',
    # packages=find_namespace_packages(where='src')
    packages=['foundations', 'algorithms']
)