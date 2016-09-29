from setuptools import setup

setup(
    name='performline',
    version='0.1.0.alpha1',
    py_modules=['performline'],
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        performline=performline.cli
    ''',
)
