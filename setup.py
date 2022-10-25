from setuptools import setup, find_packages

setup(
    name='opentrons_functions',
    version='0.2.7',
    description='A collection of functions compatible with the Opentrons API',
    url='https://github.com/tanaes/opentrons_functions',
    author='Jon G Sanders',
    author_email='jonsan@gmail.com',
    license='MIT License',
    packages=find_packages(),
    install_requires=[],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X'
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
)
