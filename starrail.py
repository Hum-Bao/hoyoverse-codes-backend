from __future__ import annotations

from typing import TYPE_CHECKING

from hoyogame import HoYoGame

if TYPE_CHECKING:
    from logging import Logger


class HSR(HoYoGame):
    def __init__(
        self,
        logger: Logger | None = None,
    ) -> None:
        url_dict = {
            "prydwen": "https://www.prydwen.gg/star-rail/",
            "gamesradar": "https://www.gamesradar.com/honkai-star-rail-codes-redeem/",
            "game8": "https://game8.co/games/Honkai-Star-Rail/archives/410296",
            "pcgamer": "https://www.pcgamer.com/honkai-star-rail-codes/",
            "eurogamer": "https://www.eurogamer.net/honkai-star-rail-codes-livestream-active-working-how-to-redeem-9321",
            "fandom": "https://honkai-star-rail.fandom.com/wiki/Redemption_Code",
        }
        super().__init__(
            name="HSR",
            url_dict=url_dict,
            base_url="https://sg-hkrpg-api.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?",
            logger=logger,
        )
