from setuptools import setup

setup(
    name='clea',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'clea=app:main'
        ]
    }
) 