from setuptools import setup, find_namespace_packages

setup(
    name='dockerinspect',
    version='0.1',
    description='Docker utility code for analysing images',
    url='https://github.com/agentreno/docker-base-detection',
    author='Karl Hopkinson-Turrell',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=[
        'requests'
    ],
    zip_safe=False
)
