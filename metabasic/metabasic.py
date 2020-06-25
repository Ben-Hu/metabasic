import json
import urllib.parse
from typing import Any, Dict, Optional

import inquirer
import requests
from pandas import DataFrame

from .exceptions import AuthError, ConfigError


class Metabasic(object):
    """Instantiates a new Metabasic Client

    Arguments:
        domain (str): The domain of the metabase host (i.e. http://my-metabase-host.com)
        session_id (Optional[str]): The metabase session id.
        database_id (Optional[int]): The metabase database id.
    """

    def __init__(
        self,
        domain: str,
        session_id: Optional[str] = None,
        database_id: Optional[int] = None,
    ):
        self.domain: str = domain
        self.session_id: Optional[str] = session_id
        self.database_id: Optional[int] = database_id

    def query(self, query: str) -> Dict[Any, Any]:
        """Queries the currently selected database.

        Arguments:
            query (str): The query to run against the currently selected database.

        Raises:
            AuthError: Raised if the client is unauthenticated.
            ConfigError: Raised if the client is unconfigured.
            Exception: Raised if an unexpected response is received.

        Returns:
            (List[List[Any]]): The results of the query.
        """
        self.__check_auth()
        self.__check_config()

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Metabase-Session": self.session_id,
        }

        body: Dict[str, Any] = {
            "database": self.database_id,
            "native": {"query": query},
            "type": "native",
        }

        data = "query=" + urllib.parse.quote(json.dumps(body))

        resp = requests.post(
            f"{self.domain}/api/dataset/json", data=data, headers=headers
        )

        if resp.status_code != 202:
            raise Exception(resp)

        return resp.json()

    def get_dataframe(self, query: str) -> DataFrame:
        """Queries the currently selected database, returning a Pandas DataFrame.

        Arguments:
            query (str): The query to run against the currently selected database.

        Returns:
            pd.DataFrame: The results of the query wrapped into a Pandas DataFrame.
        """

        res = self.query(query)

        df = DataFrame(res)

        return df

    def authenticate(self, email: str, password: str) -> "Metabasic":
        """Authenticates the client instance with the given email & password.

        Arguments:
            email (str): The email address to authenticate with.
            password (str): The password to authenticate with.

        Raises:
            Exception: Raised if an unexpected response is received.
        """
        headers = {"Content-Type": "application/json"}
        body = {"username": email, "password": password}
        resp = requests.post(f"{self.domain}/api/session", json=body, headers=headers)

        if resp.status_code != 200:
            raise Exception(resp)

        self.session_id = resp.json()["id"]

        return self

    def select_database(self) -> "Metabasic":
        """Start an interactive selection of available databases

        Raises:
            AuthError: Raised if the client is unauthenticated.
            Exception: Raised if an unexpected response is received.
        """
        self.__check_auth()

        headers = {
            "Content-Type": "application/json",
            "X-Metabase-Session": self.session_id,
        }

        resp = requests.get(f"{self.domain}/api/database", headers=headers)

        if resp.status_code != 200:
            raise Exception(resp)

        databases = {db["name"]: db["id"] for db in resp.json()}

        prompt = [inquirer.List("name", message="Database", choices=databases.keys())]
        target = inquirer.prompt(prompt)

        self.database_id = databases[target["name"]]

        return self

    def __check_auth(self):
        if not self.session_id:
            raise AuthError(
                "Client is unauthenticated.",
                "Provide a session_id or start a new session with the authenticate method.",
            )

    def __check_config(self):
        if not self.database_id:
            raise ConfigError(
                "Client is not configured",
                "Provide a database_id or select a one with the select_database method.",
            )
