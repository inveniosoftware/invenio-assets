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

Default values are set for following configuration keys during the
initialization:

* ``REQUIREJS_BASEURL`` -  a directory that AMD modules will be loaded from.
  See http://webassets.readthedocs.io/en/latest/builtin_filters.html#requirejs
  for more information on how to configure requirejs.
  (default: ``app.static_folder``)
* ``COLLECT_STATIC_ROOT`` - a path to folder for collecting static files.
  See http://flask-collect.readthedocs.io/en/latest/config.html
  (default: ``app.static_folder``)
* ``COLLECT_STORAGE`` - an import path to storage backend.
  See http://flask-collect.readthedocs.io/en/latest/config.html
  (default: ``'flask_collect.storage.link'``)
