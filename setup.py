from setuptools import setup, find_packages



setup(
    name='sbspk',
    version='0.1',

    description='Retrieve small body SPICE SPK kernels from the JPL Horizons system.',
    long_description='',

    url='https://github.com/arkhebuz/sbspk',

    author='Aleksander Tuzik',
    author_email='aleksander.tuzik@gmail.com',

    license='MIT',

    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Astronomy',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='astronomy horizons spice kernels',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['pexpect'],

    entry_points = {
        'console_scripts': ['sbspk=sbspk.command_line:main'],
    }
)
