from typing import Any, Dict, Optional

import inquirer
import requests


class Metabasic(object):
    def __init__(
        self,
        domain: str,
        session_id: Optional[str] = None,
        database_id: Optional[int] = None,
    ):
        self.domain: str = domain
        self.session_id: Optional[str] = session_id
        self.database_id: Optional[int] = database_id

    def query(self, query: str):
        headers = {
            "Content-Type": "application/json",
            "X-Metabase-Session": self.session_id,
        }

        body: Dict[str, Any] = {
            "database": self.database_id,
            "native": {"query": query},
            "type": "native",
        }

        resp = requests.post(f"{self.domain}/api/dataset", json=body, headers=headers)

        if resp.status_code != 202:
            raise Exception(resp)

        return resp.json()["data"]["rows"]

    def authenticate(self, email: str, password: str) -> None:
        headers = {"Content-Type": "application/json"}
        body = {"username": email, "password": password}
        resp = requests.post(f"{self.domain}/api/session", json=body, headers=headers)

        if resp.status_code != 200:
            raise Exception(resp)

        self.session_id = resp.json()["id"]

    def select_database(self) -> None:
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
