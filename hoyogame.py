from __future__ import annotations

import os
import time
from typing import TYPE_CHECKING

import requests
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from logging import Logger
    from pathlib import Path


class HoYoGame:
    NAME: str
    URL_DICT: dict
    BASE_URL: str
    ACTIVE_FILE: str
    EXPIRED_FILE: str

    LOGGER = None

    def __init__(
        self,
        name: str,
        url_dict: dict[str, str],
        base_url: str,
        logger: Logger | None = None,
    ) -> None:
        self.NAME = name
        self.URL_DICT = url_dict
        self.BASE_URL = base_url
        self.LOGGER = logger

        self.ACTIVE_FILE = self.NAME + ".txt"
        self.EXPIRED_FILE = self.NAME + "_exp.txt"

    def get_website_html(self) -> dict:
        """Fetch and parse HTML content from URLs defined in URL_DICT.

        Returns
        -------
        dict
            A dictionary containing BeautifulSoup objects for each URL.

        """
        requests_dict = {}
        for key, value in self.URL_DICT.items():
            requests_dict[key] = BeautifulSoup(
                requests.get(value).content,
                "html.parser",
            )
        return requests_dict

    def retrieve_codes(self, active_set: set[str]) -> None:
        requests_dict = self.get_website_html()

        for key, value in requests_dict.items():
            match key:
                case "prydwen":
                    codes = value.find_all("p", class_="code")
                    for code in codes:
                        code_text = code.text
                        if code_text.find("NEW!") != -1:
                            code_text = code_text.replace("NEW!", "").strip()
                        active_set.add(code_text.upper().strip())
                case "gamesradar":
                    strong_tags = value.find_all("strong")
                    for code_text in strong_tags:
                        if " " not in code_text.text and code_text.text != "":
                            active_set.add(code_text.text.upper().strip())
                case "game8":
                    clipboard_text = value.find_all(
                        "input",
                        class_="a-clipboard__textInput",
                    )
                    for code in clipboard_text:
                        code_text = code.get("value", "").strip()
                        if code_text and " " not in code_text:
                            active_set.add(code_text.upper().strip())
                case "pcgamer":
                    # Remove all del tags as pcgamer uses <strong> tags inside of <del> tags,
                    # making a simple <strong> search impossible
                    del_tags = value.find_all("del")
                    for tag in del_tags:
                        tag.decompose()

                    strong_tags = value.find_all("strong")
                    for tag in strong_tags:
                        code_text = tag.text.strip()
                        if code_text.isupper() and len(code_text) > 5:
                            active_set.add(code_text.upper().strip())
                case "eurogamer":
                    strong_list = value.find_all("strong")
                    for code_text in strong_list:
                        if " " not in code_text.text and code_text.text.isupper():
                            active_set.add(code_text.text.upper().strip())
                case "fandom":
                    # Remove expired codes
                    old_codes = value.find_all("td", class_="bg-old")
                    for old_code in old_codes:
                        old_code.parent.decompose()

                    codes = value.find_all("code")
                    for code_text in codes:
                        active_set.add(code_text.text.upper().strip())
                case _:
                    return

    def verify_codes(self, active_set: set, expired_set: set) -> None:
        url = (
            self.BASE_URL
            + "lang="
            + os.getenv(self.NAME + "_LANG", "")
            + "&game_biz="
            + os.getenv(self.NAME + "_GAMEBIZ", "")
            + "&uid="
            + os.getenv(self.NAME + "_UID", "")
            + "&region="
            + os.getenv(self.NAME + "_REGION", "")
            + "&cdkey="
        )

        cookies = {
            "token": "account_mid_v2="
            + os.getenv("ACCOUNT_MID_V2", "")
            + "; "
            + "account_id_v2="
            + os.getenv("ACCOUNT_ID_V2", "")
            + "; "
            + "cookie_token_v2="
            + os.getenv("COOKIE_TOKEN_V2", ""),
        }

        # {'retcode': 0, 'message': 'OK', 'data': {'msg': 'Redeemed successfully'}}
        # {'data': None, 'message': 'Redemption code expired.', 'retcode': -2001}
        # {'data': null, 'message': 'The redemption code is no longer valid.', 'retcode': -2002}
        # {'data': null, 'message': 'Invalid redemption code.', 'retcode': -2003}
        # {'data': None, 'message': 'Redemption code has already been used', 'retcode': -2017}
        # {'data': None, 'message': 'Redemption code has already been used', 'retcode': -2018}
        # {"data": null, 'message': 'This code cannot be redeemed on this platform', 'retcode': -2024}
        # {"data":null,"message":"error found(error code -1048)","retcode":-1048}

        for code in active_set:
            get_request = requests.get((url + code), cookies=cookies)
            if (
                "OK" not in get_request.text
                and "-2018" not in get_request.text
                and "-2017" not in get_request.text
                and "platform" not in get_request.text
            ):
                if self.LOGGER is not None:
                    self.LOGGER.info("EXPIRED: %s | %s", code, get_request.text)
                expired_set.add(code)
            else:
                if self.LOGGER is not None:
                    self.LOGGER.info("VALID: %s | %s", code, get_request.text)

            time.sleep(20)

    @staticmethod
    def remove_expired(active_set: set[str], expired_set: set[str]) -> None:
        """Remove expired codes from the active set.

        Parameters
        ----------
        active_set : set[str]
            Set of currently active codes
        expired_set : set[str]
            Set of expired codes to remove

        """
        active_set.difference_update(expired_set)

    @staticmethod
    def write_file(path: Path, write_set: set, file: str) -> None:
        with (path / file).open("w", encoding="utf-8") as f:
            if write_set:
                f.write("\n".join(sorted(write_set)))
                f.write("\n")
                f.truncate(f.tell() - len(os.linesep))
            f.close()

    def run(self, path: Path) -> None:
        expired_set = set()
        active_set = set()

        if not (path / self.EXPIRED_FILE).exists():
            if self.LOGGER is not None:
                self.LOGGER.error(
                    "Required file %s not found at %s",
                    self.EXPIRED_FILE,
                    path,
                )
            with (path / self.EXPIRED_FILE).open("w"):
                pass
            if self.LOGGER is not None:
                self.LOGGER.info("Created empty file: %s", self.EXPIRED_FILE)

        if not (path / self.ACTIVE_FILE).exists():
            if self.LOGGER is not None:
                self.LOGGER.error(
                    "Required file %s not found at %s",
                    self.ACTIVE_FILE,
                    path,
                )
            with (path / self.ACTIVE_FILE).open("w"):
                pass
            if self.LOGGER is not None:
                self.LOGGER.info("Created empty file: %s", self.ACTIVE_FILE)

        with (path / self.EXPIRED_FILE).open() as f:
            expired_set = {line.strip() for line in f}
        self.retrieve_codes(active_set)
        self.remove_expired(active_set, expired_set)
        self.verify_codes(active_set, expired_set)
        HoYoGame.remove_expired(active_set, expired_set)
        HoYoGame.write_file(path, active_set, self.ACTIVE_FILE)
        HoYoGame.write_file(path, expired_set, self.EXPIRED_FILE)
