from setuptools import setup

setup(
    name='performline',
    version='0.1.0a1',
    py_modules=['performline'],
    url='https://github.com/PerformLine/python-performline-client',
    install_requires=[
        'click==6.6',
        'requests==2.11.1',
        'pytest',
        'flake8',
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
