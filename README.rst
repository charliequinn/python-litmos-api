========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        | |coveralls| |codecov|
        | |landscape|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/python-litmos-api/badge/?style=flat
    :target: https://readthedocs.org/projects/python-litmos-api
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/charliequinn/python-litmos-api.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/charliequinn/python-litmos-api

.. |coveralls| image:: https://coveralls.io/repos/charliequinn/python-litmos-api/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/charliequinn/python-litmos-api

.. |codecov| image:: https://codecov.io/github/charliequinn/python-litmos-api/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/charliequinn/python-litmos-api

.. |landscape| image:: https://landscape.io/github/charliequinn/python-litmos-api/master/landscape.svg?style=flat
    :target: https://landscape.io/github/charliequinn/python-litmos-api/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/litmos-api.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/litmos-api

.. |downloads| image:: https://img.shields.io/pypi/dm/litmos-api.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/litmos-api

.. |wheel| image:: https://img.shields.io/pypi/wheel/litmos-api.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/litmos-api

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/litmos-api.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/litmos-api

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/litmos-api.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/litmos-api


.. end-badges

Python package integrating with Litmos User and Teams API

* Free software: BSD license

Installation
============

::

    pip install litmos-api

Documentation
=============

https://python-litmos-api.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
