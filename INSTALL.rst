Installation
============

The Invenio-Assets package is on PyPI so all you need is:

.. code-block:: console

    $ pip install invenio-assets

Invenio-Asssets depends on Flask-Assets, WebAssets and Flask-Collect.


Configuration
=============
Default values are set for following configuration keys during the
initialization:

* ``REQUIREJS_BASEURL`` -  a directory that AMD modules will be loaded from.
  (default: ``app.static_folder``)
* ``COLLECT_STATIC_ROOT`` - a path to folder for collecting static files.
  (default: ``app.static_folder``)
* ``COLLECT_STORAGE`` - an import path to storage backend.
  (default: ``'flask_collect.storage.link'``)
