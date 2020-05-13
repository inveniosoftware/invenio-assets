..
    This file is part of Invenio.
    Copyright (C) 2015-2020 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Upgrade to Webpack
==================

.. note::

    Invenio-Assets v1.2.0 removed support for AMD/RequireJS and Flask-Assets
    build system.

In order to upgrade your module from AMD to Webpack, follow the steps below.

Move files to the ``assets`` folder
-----------------------------------

* Move files from ``static/js`` to the ``assets/js`` folder.
* Move files from ``static/scss`` to the ``assets/scss`` folder.
* Keep the rest of the static files in the ``static`` folder.

Change the way of importing modules
-----------------------------------
Since Webpack doesn't use ``require.js``, you should change the way modules
are imported in the JavaScript files. The example below shows how to
import the modules:

.. code-block:: javascript

    import my-module from 'path/to/my/module'


Create a WebpackBundle
----------------------
The `Flask-WebpackExt <https://flask-webpackext.readthedocs.io/en/latest/>`_
package provides a class
:class:`flask_webpackext.bundle.WebpackBundle` for declaring the needed
assets and NPM dependencies of each one of your modules. This class replaces
the old bundles.

.. code-block:: python

    # webpack.py
    from flask_webpackext import WebpackBundle
    mybundle = WebpackBundle(
        __name__,
        './modules/module1/static',
        entry={
            'module1-app': './js/module1-app.js',
        },
        dependencies={
            'jquery': '^3.2.1'
        }
    )


Add a new entry point
---------------------
You should remove the previous entry point (i. e. ``invenio_assets.bundles``)
from ``setup.py``. Then, you should add the new entry point,
``invenio_assets.webpack``, and include the bundle you created in the previous
step.

.. code-block:: python

   # setup.py
   setup(
       # ...
       entry_points={
           'invenio_assets.webpack': [
               'mybundle = mypackage.webpack:mybundle',
           ],
           # ...
        }
        # ...
    )

Invenio-Assets will automatically load bundles defined by the entry point
group ``invenio_assets.webpack``.


Run the webpack commands
------------------------
In order to build the assets you need to run the following command:

.. code-block:: console

    $ flask webpack buildall

This command will copy all files from the ``assets`` folder to the application
instance folder designated for the Webpack project, download the npm packages
and run Webpack to build the assets.

To collect the static files from the ``static`` folder, you need to run the
command below:

.. code-block:: console

    $ flask collect -v
