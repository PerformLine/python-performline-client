from setuptools import setup, find_packages

setup(
    name='performline',
    description='Client library for using the public PerformMatch Compliance API',
    version='0.1.0a7',
    author='PerformLine Engineering',
    author_email='tech+api@performline.com',
    url='https://github.com/PerformLine/python-performline-client',
    install_requires=[
        'click',
        'requests',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'performline=performline.cli:main',
        ],
    },
    packages=find_packages(exclude=['*.tests']),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Office/Business',
        'Environment :: Console',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Customer Service',
        'Intended Audience :: Financial and Insurance Industry',
    ],
)
