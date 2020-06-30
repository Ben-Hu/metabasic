# 0.X.Y (2020-MM-DD)
### Enhancements
  - Adding `raw_query(query, export_format)` to retrieve responses in one of the supported export formats for `/api/dataset/{export_format}` (`csv`, `json`, `xslx`)

### Bug fix
  - `get_dataframe` uses `raw_query` with `export_format="csv"` to guarantee that the result set has a column ordering equal to the ordering specified by the query statement

# 0.4.2 (2020-06-24)
### Enhancements
  - Adding use of api/dataset/json to circumvent metabase row limit of 2000

# 0.4.0 (2020-05-11)
### Enhancements
  - Adds get_dataframe utility method, returning a pandas DataFrame
  - Updates query method to return the raw 'data' of the API resposne


# 0.3.0 (2020-05-10)
### Enhancements
  - Update authenticate & select_database methods to allow chaining


# 0.2.0 (2020-05-09)
### Enhancements
  - Add better handling of unconfigured/unauthenticated clients


# 0.1.0 (2020-05-09)
### Enhancements
  - Initial version