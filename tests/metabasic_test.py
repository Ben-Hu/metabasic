from unittest.mock import Mock

import pytest
from pandas import DataFrame
from requests import Response

from metabasic import Metabasic
from metabasic.exceptions import AuthError, ConfigError


class TestQuery:
    @pytest.fixture
    def metabasic(self):
        return Metabasic("domain", session_id="123abc", database_id=123)

    def test_query_success(self, mocker, metabasic):
        json = [{"a": 1}, {"b": 2}, {"c": 3}]

        mock_response = Mock(Response, json=lambda: json)
        mock_response.status_code = 202
        mocker.patch("requests.post", return_value=mock_response)

        print(metabasic.query("SELECT * FROM tests"))

        assert metabasic.query("SELECT * FROM tests") == json

    def test_query_error(self, mocker, metabasic):
        mock_response = Mock(Response)
        mock_response.status_code = 401
        mocker.patch("requests.post", return_value=mock_response)

        with pytest.raises(Exception, match=str(mock_response)):
            metabasic.query("SELECT * FROM tests")

    def test_unconfigured(self, mocker):
        metabasic = Metabasic("domain", session_id="123abc")

        with pytest.raises(Exception, match=str(ConfigError())):
            metabasic.query("SELECT * FROM tests")

    def test_unauthenticated(self, mocker):
        metabasic = Metabasic("domain", database_id=123)

        with pytest.raises(Exception, match=str(AuthError())):
            metabasic.query("SELECT * FROM tests")


class TestGetDataFrame:
    @pytest.fixture
    def metabasic(self):
        return Metabasic("domain", session_id="123abc", database_id=123)

    def test_get_dataframe_success(self, mocker, metabasic):
        json = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]

        mock_response = Mock(Response, json=lambda: json)
        mock_response.status_code = 202

        mocker.patch("requests.post", return_value=mock_response)
        expected = DataFrame(json)

        result = metabasic.get_dataframe("SELECT * FROM tests")
        assert isinstance(result, DataFrame)
        assert result.to_dict() == expected.to_dict()

    def test_get_dataframe_error(self, mocker, metabasic):
        mock_response = Mock(Response)
        mock_response.status_code = 401
        mocker.patch("requests.post", return_value=mock_response)

        with pytest.raises(Exception, match=str(mock_response)):
            metabasic.get_dataframe("SELECT * FROM tests")

    def test_unconfigured(self, mocker):
        metabasic = Metabasic("domain", session_id="123abc")

        with pytest.raises(Exception, match=str(ConfigError())):
            metabasic.get_dataframe("SELECT * FROM tests")

    def test_unauthenticated(self, mocker):
        metabasic = Metabasic("domain", database_id=123)

        with pytest.raises(Exception, match=str(AuthError())):
            metabasic.get_dataframe("SELECT * FROM tests")


class TestAuthenticate:
    @pytest.fixture
    def metabasic(self):
        return Metabasic("domain")

    def test_authenticate_success(self, mocker, metabasic):
        mock_response = Mock(Response, json=lambda: {"id": "abc123"})
        mock_response.status_code = 200
        mocker.patch("requests.post", return_value=mock_response)

        result = metabasic.authenticate("email", "password")
        assert isinstance(result, Metabasic)
        assert metabasic.session_id == "abc123"

    def test_authenticate_error(self, mocker, metabasic):
        mock_response = Mock(Response)
        mock_response.status_code = 401
        mocker.patch("requests.post", return_value=mock_response)

        with pytest.raises(Exception, match=str(mock_response)):
            metabasic.authenticate("email", "password")


class TestSelectDatabase:
    @pytest.fixture
    def metabasic(self):
        return Metabasic("domain", session_id="123abc", database_id=123)

    def test_select_database_success(self, mocker, metabasic):
        databases = [{"id": 1, "name": "foo"}, {"id": 2, "name": "bar"}]

        mock_response = Mock(Response, json=lambda: databases)
        mock_response.status_code = 200
        mocker.patch("requests.get", return_value=mock_response)

        mocker.patch("inquirer.prompt", return_value={"name": "foo"})
        result = metabasic.select_database()

        assert isinstance(result, Metabasic)
        assert metabasic.database_id == 1

    def test_select_database_error(self, mocker, metabasic):
        mock_response = Mock(Response)
        mock_response.status_code = 401
        mocker.patch("requests.get", return_value=mock_response)

        with pytest.raises(Exception, match=str(mock_response)):
            metabasic.select_database()

    def test_unauthenticated(self, mocker):
        metabasic = Metabasic("domain", database_id=123)

        with pytest.raises(Exception, match=str(AuthError())):
            metabasic.select_database()
