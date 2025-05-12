# hsr-codes-backend
Backend for [HoYoverse-Codes](https://github.com/Hum-Bao/hoyoverse-codes). Finds and validates redemption codes for miHoYo games.

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

# Honkai: Star Rail:
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

# Genshin Impact:
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

