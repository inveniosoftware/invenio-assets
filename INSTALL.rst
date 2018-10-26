..
    This file is part of Invenio.
    Copyright (C) 2015-2018 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Installation
============

Invenio-Assets is on PyPI so all you need is:

.. code-block:: console

   $ pip install invenio-assets

Invenio-Assets depends on Flask-WebpackExt, Flask-Assets, WebAssets and
Flask-Collect.

In order to build the assets, you can choose between using:

* `Flask-WebpackExt <https://flask-webpackext.readthedocs.io/en/latest/>`_;
* `Flask-Assets <https://flask-assets.readthedocs.io/en/latest/>`_.
  By choosing this option, you will also have many filters which depend on
  existing command line tools to be installed such as RequireJS, UglifyJS,
  Node-SASS and CleanCSS. These tools are most easily installed with NPM:

.. code-block:: console

    $ npm update
    $ npm install -g node-sass clean-css clean-css-cli uglify-js \
        requirejs

