# HoYoverse-Codes-Backend
Backend for [HoYoverse-Codes](https://github.com/Hum-Bao/hoyoverse-codes). Finds and validates redemption codes for miHoYo games.

## Table of Contents
- [Requirements](#requirements)
- [Honkai: Star Rail](#honkai-star-rail)
- [Genshin Impact](#genshin-impact)
- [Zenless Zone Zero](#zenless-zone-zero)
- [GitHub](#github)

## Requirements
Requires the following Python libraries:
```
PyGithub
python-dotenv
beautifulsoup4
requests
```

Requires the following fields in a .env file:
```
ACCOUNT_MID_V2 = ""
ACCOUNT_ID_V2 = ""
COOKIE_TOKEN_V2 = ""
```

## Honkai: Star Rail:
These fields are required for validating and redeeming HSR redemption codes:
```
HSR_UID = ""
HSR_LANG = ""
HSR_GAMEBIZ = ""
HSR_REGION = ""
```
The defaults for USA are:
```
HSR_LANG = "en"
HSR_GAMEBIZ = "hkrpg_global"
HSR_REGION = "prod_official_usa"
```

## Genshin Impact:
These fields are required for validating and redeeming Genshin Impact redemption codes:
```
GENSHIN_UID = ""
GENSHIN_LANG = ""
GENSHIN_GAMEBIZ = ""
GENSHIN_REGION = ""
```
The defaults for USA are:
```
GENSHIN_LANG = "en"
GENSHIN_GAMEBIZ = "hk4e_global"
GENSHIN_REGION = "os_usa"
```

## Zenless Zone Zero:
These fields are required for validating and redeeming ZZZ redemption codes:
```
ZZZ_UID = ""
ZZZ_LANG = ""
ZZZ_GAMEBIZ = ""
ZZZ_REGION = ""
```
The defaults for USA are:
```
ZZZ_LANG = "en"
ZZZ_GAMEBIZ = "nap_global"
ZZZ_REGION = "prod_gf_us"
```

## GitHub:
These fields are required for pushing updates to GitHub
```
GITHUB_TOKEN = ""
GITHUB_REPO = ""
```

