# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='unibuddy',
    version='0.0.1',
    description='Unicode utility functions.',
    long_description=readme,
    author='Floor Is Lava',
    author_email='lava@floor.is',
    url='https://github.com/joshleejosh/unibuddy',
    license=license,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Internationalization',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Localization',
        'Topic :: Text Processing :: Fonts',
        'Topic :: Text Processing :: General',
        'Topic :: Utilities',
        ],
    packages=find_packages(exclude=('tests', 'docs', 'data'))
)
