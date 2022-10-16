from setuptools import setup
from shutil import rmtree

# with open('README.md') as f:
    # readme = f.read()
try:
    print('removing build files')
    rmtree('build')
    rmtree('dist')
except Exception as e:
    print(e)

setup(
    name="Mazes",
    version='0.0.2',
    description='Mazes for Programmers - Python',
    author='Rob Weddell',
    packages=['maze_structures', 'maze_algorithms']
)