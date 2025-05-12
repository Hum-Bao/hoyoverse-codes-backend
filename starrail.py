import os
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

HSR_ACTIVE = "hsr.txt"
HSR_EXPIRED = "hsr_exp.txt"


def get_website_html() -> dict:
    url_dict = {
        "prydwen": "https://www.prydwen.gg/star-rail/",
        "gamesradar": "https://www.gamesradar.com/honkai-star-rail-codes-redeem/",
        "game8": "https://game8.co/games/Honkai-Star-Rail/archives/410296",
        "pcgamer": "https://www.pcgamer.com/honkai-star-rail-codes/",
        "eurogamer": "https://www.eurogamer.net/honkai-star-rail-codes-livestream-active-working-how-to-redeem-9321",
        "fandom": "https://honkai-star-rail.fandom.com/wiki/Redemption_Code",
    }

    requests_dict = {}
    for key, value in url_dict.items():
        requests_dict[key] = BeautifulSoup(
            requests.get(value).content,
            "html.parser",
        )
    return requests_dict


def retrieve_codes(active_codes_set: set) -> None:
    requests_dict = get_website_html()

    for key, value in requests_dict.items():
        match key:
            case "prydwen":
                codes = value.find_all("p", class_="code")
                for code in codes:
                    code_text = code.text
                    if code_text.find("NEW!") != -1:
                        code_text = code_text.replace("NEW!", "").strip()
                    active_codes_set.add(code_text)
            case "gamesradar":
                strong_tags = value.find_all("strong")
                for code_text in strong_tags:
                    if " " not in code_text.text and code_text.text != "":
                        active_codes_set.add(code_text.text)
            case "game8":
                clipboard_text = value.find_all(
                    "input",
                    class_="a-clipboard__textInput",
                )
                for code in clipboard_text:
                    code_text = code.get("value", "").strip()
                    if code_text and " " not in code_text:
                        active_codes_set.add(code_text)
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
                        active_codes_set.add(code_text)
            case "eurogamer":
                strong_list = value.find_all("strong")
                for code_text in strong_list:
                    if " " not in code_text.text and code_text.text.isupper():
                        active_codes_set.add(code_text.text)
            case "fandom":
                # Remove expired codes
                old_codes = value.find_all("td", class_="bg-old")
                for old_code in old_codes:
                    old_code.parent.decompose()

                codes = value.find_all("code")
                for code_text in codes:
                    active_codes_set.add(code_text.text.upper())
            case _:
                return


def verify_codes(active_set: set, expired_set: set) -> None:
    base_url = (
        "https://sg-hkrpg-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?"
    )

    url = (
        base_url
        + "lang="
        + os.getenv("HSR_LANG", "")
        + "&game_biz="
        + os.getenv("HSR_GAMEBIZ", "")
        + "&uid="
        + os.getenv("HSR_UID", "")
        + "&region="
        + os.getenv("HSR_REGION", "")
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
    # {"data": null, 'message': 'Invalid redemption code.', 'retcode': -2003}
    # {"data": None, "message": "Redemption code has already been used", "retcode": -2018}
    # {'data': None, 'message': 'Redemption code has already been used', 'retcode': -2017}

    for code in active_set:
        get_request = requests.get((url + code), cookies=cookies)
        if (
            "OK" not in get_request.text
            and "-2018" not in get_request.text
            and "-2017" not in get_request.text
        ):
            print("EXPIRED: " + code)
            print(get_request.text)
            expired_set.add(code)
        else:
            print("VALID: " + code)
            print(get_request.text)
        time.sleep(20)


def remove_expired(active_set: set, expired_set: set) -> None:
    active_set.difference_update(expired_set)


def write_expired(path: Path, expired_set: set) -> None:
    with (path / HSR_EXPIRED).open("w", encoding="utf-8") as f:
        for exp in expired_set:
            f.write(exp + "\n")
        f.truncate(f.tell() - len(os.linesep))


def write_codes(path: Path, active_set: set) -> None:
    # Sort codes to allow for consistent ordering when pushing to GitHub
    with (path / HSR_ACTIVE).open("w", encoding="utf-8") as f:
        for code in sorted(active_set):
            f.write(code + "\n")
        f.truncate(f.tell() - len(os.linesep))
        f.close()


def main(path: Path) -> None:
    expired_set = set()
    active_set = set()
    with (path / HSR_EXPIRED).open() as f:
        expired_set = {line.strip() for line in f}
    retrieve_codes(active_set)
    remove_expired(active_set, expired_set)
    verify_codes(active_set, expired_set)
    remove_expired(active_set, expired_set)
    write_codes(path, active_set)
    write_expired(path, expired_set)
