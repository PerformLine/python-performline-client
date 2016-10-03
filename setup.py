from setuptools import setup

setup(
    name='performline',
    version='0.1.0a1',
    py_modules=['performline'],
    url='https://github.com/PerformLine/python-performline-client',
    install_requires=[
        'click==6.6',
        'requests==2.11.1',
    ],
    tests_require=[
        'argcomplete>=1.4.1,<1.5.0',
        'configparser==3.5.0',
        'enum34==1.1.6',
        'flake8==3.0.4',
        'mccabe==0.5.2',
        'py==1.4.31',
        'pycodestyle==2.0.0',
        'pyflakes==1.2.3',
        'pytest==3.0.2',
    ],
    entry_points={
        'console_scripts': [
            'performline=performline.cli',
        ],
    },
    packages=[
        'performline',
    ],
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
