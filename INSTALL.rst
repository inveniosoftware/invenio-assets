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

Invenio-Asssets depends on Flask-Assets, WebAssets and Flask-Collect. Also,
many filters depends on existing command line tools to be installed such as
RequireJS, UglifyJS, Node-SASS and CleanCSS. These tools are most easily
installed with NPM, e.g.:

.. code-block:: console

   $ npm update
   $ npm install -g node-sass clean-css clean-css-cli uglify-js \
     requirejs
