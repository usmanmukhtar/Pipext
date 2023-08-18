from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='pipext',
    version='0.2.1',
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
    long_description=long_description,
    long_description_content_type="text/markdown", 
)
