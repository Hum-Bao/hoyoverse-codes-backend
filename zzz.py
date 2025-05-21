from __future__ import annotations

from typing import TYPE_CHECKING

from hoyogame import HoYoGame

if TYPE_CHECKING:
    from logging import Logger


class ZZZ(HoYoGame):
    def __init__(
        self,
        logger: Logger | None = None,
    ) -> None:
        url_dict = {
            "gamesradar": "https://www.gamesradar.com/games/action-rpg/zenless-zone-zero-codes/",
            "game8": "https://game8.co/games/Zenless-Zone-Zero/archives/435683",
            "pcgamer": "https://www.pcgamer.com/games/action/zenless-zone-zero-codes/",
            "eurogamer": "https://www.eurogamer.net/zenless-zone-zero-codes-how-to-redeem",
            "fandom": "https://zenless-zone-zero.fandom.com/wiki/Redemption_Code",
        }
        super().__init__(
            name="ZZZ",
            url_dict=url_dict,
            base_url="https://public-operation-nap.hoyoverse.com/common/apicdkey/api/webExchangeCdkey?",
            logger=logger,
        )
