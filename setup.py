#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'wheel',
    'PyYAML',
    'docopt'
]

test_requirements = [
]

setup(
    name='SmartFileSorter',
    version='0.4.0',
    description='Rule based file moving and renaming tool',
    long_description=readme + '\n\n' + history,
    author='Jason Short',
    author_email='jason@sheersky.com',
    url='https://github.com/jashort/SmartFileSorter',
    packages=[
        'smartfilesorter',
        'smartfilesorter.actionplugins',
        'smartfilesorter.matchplugins'
    ],
    scripts=['bin/sfs'],
    package_dir={'smartfilesorter':
                 'smartfilesorter'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='smartfilesorter',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Utilities'
    ],
    test_suite='tests',
    tests_require=test_requirements
)
