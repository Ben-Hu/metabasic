Metabasic
=========
Dead simple client for interacting with the Metabase dataset API

.. image :: https://circleci.com/gh/Ben-Hu/metabasic.svg?style=svg
  :target: https://circleci.com/gh/Ben-Hu/metabasic

.. image :: https://github.com/Ben-Hu/metabasic/workflows/ci/badge.svg
  :target: https://github.com/Ben-Hu/metabasic/actions

.. image :: https://codecov.io/gh/Ben-Hu/metabasic/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/Ben-Hu/metabasic

.. image :: https://img.shields.io/lgtm/grade/python/g/Ben-Hu/metabasic.svg?logo=lgtm&logoWidth=18
  :target: https://lgtm.com/projects/g/Ben-Hu/metabasic/context:Python

.. image :: https://img.shields.io/github/license/Ben-Hu/metabasic
  :target: https://github.com/Ben-Hu/metabasic/blob/master/LICENSE

.. image :: https://img.shields.io/github/v/tag/Ben-Hu/metabasic
  :target: https://github.com/Ben-Hu/metabasic/releases

.. image :: https://img.shields.io/pypi/v/metabasic?color=blue
  :target: https://pypi.org/project/metabasic


Install
-------
::

  pip install metabasic


Examples
--------
.. code:: python

  from metabasic import Metabasic
  domain = "https://my-metabase-domain.com"

  # Authentication with an existing session
  db = Metabasic(domain, session_id="foo" database_id=1)
  db.query("SELECT * FROM bar")

  # Email/Password authentication
  ga = Metabasic(domain, database_id=2)
  ga.authenticate("foo@email.com", "password")
  ga_query = {
      "ids": "ga:1234567890",
      "start-date": "30daysAgo",
      "end-date": "today",
      "metrics": "ga:someMetric",
      "dimensions": "ga:someDimension",
      "sort": "ga:someDimension",
      "max-results": 10000
  )
  ga.query(json.dumps(ga_query))

  # Select a database interactively
  m = Metabasic(domain, session_id="foo")
  m.select_database()

.. toctree::
  :hidden:
  :maxdepth: 1

  metabasic/modules