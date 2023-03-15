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

Invenio-Assets depends on
`Flask-WebpackExt <https://flask-webpackext.readthedocs.io/en/latest/>`_,
`Flask-Assets <https://flask-assets.readthedocs.io/en/latest/>`_,
`WebAssets <https://webassets.readthedocs.io/en/latest/>`_
and `Flask-Collect <https://flask-collect.readthedocs.io/en/latest/>`_.

By choosing to use Flask-Assets, you will also have many filters which depend
on existing command line tools to be installed such as RequireJS, UglifyJS,
SASS and CleanCSS. These tools are most easily installed with
`NPM <https://nodejs.org/en/download/>`_:

.. code-block:: console

    $ npm update
    $ npm install -g sass clean-css clean-css-cli uglify-js \
        requirejs

