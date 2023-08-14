from setuptools import setup, find_packages

setup(
    name='pipext',
    version='0.1',
    packages=find_packages(),
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'pipext=pipext.main:main',
        ],
    },
    author='Usman Mukhtar',
    description='An extended pip installer that updates requirements.txt',
)
