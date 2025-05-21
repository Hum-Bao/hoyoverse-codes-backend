from __future__ import annotations

from typing import TYPE_CHECKING

from hoyogame import HoYoGame

if TYPE_CHECKING:
    from logging import Logger


class Genshin(HoYoGame):
    def __init__(
        self,
        logger: Logger | None = None,
    ) -> None:
        url_dict = {
            "gamesradar": "https://www.gamesradar.com/genshin-impact-codes-redeem/",
            "game8": "https://game8.co/games/Genshin-Impact/archives/304759",
            "eurogamer": "https://www.eurogamer.net/genshin-impact-codes-livestream-active-working-how-to-redeem-9026",
            "fandom": "https://genshin-impact.fandom.com/wiki/Promotional_Code",
        }
        super().__init__(
            name="GENSHIN",
            url_dict=url_dict,
            base_url="https://public-operation-hk4e.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?",
            logger=logger,
        )
