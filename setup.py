# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2015-2020 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Media assets management for Invenio."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'pytest-invenio>=1.4.0',
    'mock>=1.3.0',
]

extras_require = {
    'docs': [
        'Sphinx>=1.5.1',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

setup_requires = [
    'pytest-runner>=2.6.2',
]

install_requires = [
    'Flask>=1.0.4,<2.0',
    'Flask-Collect==1.2.2',
    'Flask-WebpackExt>=1.0.0',
    'invenio-base>=1.2.3',
    'node-semver>=0.1.1,<0.2.0',  # FIXME troubleshooting#22
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('invenio_assets', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='invenio-assets',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='invenio assets npm collect',
    license='MIT',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/invenio-assets',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    entry_points={
        'flask.commands': [
            'collect = invenio_assets.cli:collect',
        ],
        'invenio_base.apps': [
            'invenio_assets = invenio_assets:InvenioAssets',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Development Status :: 5 - Production/Stable',
    ],
)
