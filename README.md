[![CircleCI](https://circleci.com/gh/Ben-Hu/metabasic.svg?style=svg)](https://circleci.com/gh/Ben-Hu/metabasic)
[![Actions](https://github.com/Ben-Hu/metabasic/workflows/ci/badge.svg)](https://github.com/Ben-Hu/metabasic/actions)
[![codecov](https://codecov.io/gh/Ben-Hu/metabasic/branch/master/graph/badge.svg)](https://codecov.io/gh/Ben-Hu/metabasic)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Ben-Hu/metabasic.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Ben-Hu/metabasic/context:python)
[![License](https://img.shields.io/github/license/Ben-Hu/metabasic)](https://github.com/Ben-Hu/metabasic/blob/master/LICENSE)
[![Tag](https://img.shields.io/github/v/tag/Ben-Hu/metabasic)](https://github.com/Ben-Hu/metabasic/releases)
[![PyPI](https://img.shields.io/pypi/v/metabasic?color=blue)](https://pypi.org/project/metabasic/)


# Metabasic
Dead simple client for interacting with the Metabase dataset API

## Install
```sh
pip install metabasic
```

## Examples
```python
from metabasic import Metabasic
domain = "https://my-metabase-domain.com"

# Authentication with an existing session
db = Metabasic(domain, session_id="foo", database_id=1)
db.query("SELECT * FROM bar")
db.get_dataframe("SELECT * FROM bar")

# Email/Password authentication
ga = Metabasic(domain, database_id=2).authenticate("foo@email.com", "password")
ga_query = {
    "ids": "ga:1234567890",
    "start-date": "30daysAgo",
    "end-date": "today",
    "metrics": "ga:someMetric",
    "dimensions": "ga:someDimension",
    "sort": "ga:someDimension",
    "max-results": 10000
}
ga.query(json.dumps(ga_query))

# Select a database interactively
m = (
  Metabasic(domain)
  .authenticate("foo@email.com", "password")
  .select_database()
)
```
