..
    This file is part of Invenio.
    Copyright (C) 2015-2020 CERN.

    Invenio is free software; you can redistribute it and/or modify it
    under the terms of the MIT License; see LICENSE file for more details.

Changes
=======

Version 1.2.0 (released 2020-05-13)

* Removes support for Flask-Assets and Webassets which was deprecated with
  the release of Invenio v3.0.

Version 1.1.5 (released 2020-04-28)

* Webpack now uses by default in debug/development mode folder-level symlinking
* Enabled source maps for Webpack development builds.
* Patched the ``watchpack`` library to support symlink watching via using
  ``patch-package``.

Version 1.1.4 (released 2019-02-20)

- Webpack Live-reload plugin.
- Webpack `@templates` alias.
- Webpack fix symlinks issue.

Version 1.1.3 (released 2019-07-29)

- Turn off webpack warnings

Version 1.1.2 (released 2019-02-15)

- Removes NPM warnings.

Version 1.1.1 (released 2018-12-14)

Version 1.1.0 (released 2018-11-06)

- Introduces webpack support.

Version 1.0.0 (released 2018-03-23)

- Initial public release.
