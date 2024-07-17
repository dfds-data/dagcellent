# dagcellent

[![PyPI - Version](https://img.shields.io/pypi/v/dagcellent.svg)](https://pypi.org/project/dagcellent)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dagcellent.svg)](https://pypi.org/project/dagcellent)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install dagcellent
```

## License

`dagcellent` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


Changelog Generation
--------------------

We use ``towncrier`` for tracking changes and generating a changelog.
When making a pull request, we require that you add a towncrier entry along with the code changes.
You should create a file named ``<PR number>.<change type>`` in the ``doc/changes`` directory, where the PR number should be substituted for ``<PR number>``, and ``<change type>`` is either ``feature``, ``bugfix``, ``doc``, ``removal``, ``misc``, or ``deprecation``,
depending on the type of change included in the PR.

You can also create this file by installing ``towncrier`` and running 

   towncrier create <PR number>.<change type>

Running this will create a file in the ``doc/changes`` directory with a filename corresponding to the argument you passed to ``towncrier create``.
In this file, you should add a short description of the changes that the PR introduces.
