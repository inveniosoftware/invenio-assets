..
    This file is part of Invenio.
    Copyright (C) 2017 CERN.

    Invenio is free software; you can redistribute it
    and/or modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation; either version 2 of the
    License, or (at your option) any later version.

    Invenio is distributed in the hope that it will be
    useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Invenio; if not, write to the
    Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
    MA 02111-1307, USA.

    In applying this license, CERN does not
    waive the privileges and immunities granted to it by virtue of its status
    as an Intergovernmental Organization or submit itself to any jurisdiction.


Configuration
=============

Default values are set for following configuration variables:

* ``REQUIREJS_BASEURL`` -  directory that AMD modules will be loaded from (see
  `webassets
  <http://webassets.readthedocs.io/en/latest/builtin_filters.html#requirejs>`_
  for details). Default: ``app.static_folder``.
* ``COLLECT_STATIC_ROOT`` - path to folder where static files will be
  collected to (see
  `Flask-Collect <http://flask-collect.readthedocs.io/en/latest/config.html>`_
  for details). Default: ``app.static_folder``.
* ``COLLECT_STORAGE`` - import path to Flask-Collect storage implementation
  (see
  `Flask-Collect <http://flask-collect.readthedocs.io/en/latest/config.html>`_
  for details). Default: ``'flask_collect.storage.link'`` (i.e. symlinking of
  files from source code into ``COLLECT_STATIC_ROOT``).

Note, normally in a production environment you should change
``COLLECT_STORAGE`` to ``flask_collect.storage.file`` in order to copy files
instead of symlinking them.
