import logging
from pathlib import Path

import gitpush
from dotenv import load_dotenv
from genshin import Genshin
from starrail import HSR
from zzz import ZZZ

ACTIVE_GAMES: list[str] = ["HSR", "Genshin", "ZZZ"]

GITHUB_PUSH: bool = True

GITHUB_FILES: list[str] = []


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    path = Path(__file__).parent.absolute()
    logger.info("Working directory: %s", path)

    load_dotenv()
    logger.info("Environment variables loaded")

    if "HSR" in ACTIVE_GAMES:
        logger.info("Starting HSR code check")
        hsr = HSR(logger)
        hsr.run(path)
        GITHUB_FILES.append(hsr.ACTIVE_FILE)
        logger.info("HSR code check finished")

    if "Genshin" in ACTIVE_GAMES:
        logger.info("Starting Genshin code check")
        genshin = Genshin(logger)
        genshin.run(path)
        GITHUB_FILES.append(genshin.ACTIVE_FILE)
        logger.info("Genshin code check finished")

    if "ZZZ" in ACTIVE_GAMES:
        logger.info("Starting ZZZ code check")
        zzz = ZZZ(logger)
        zzz.run(path)
        GITHUB_FILES.append(zzz.ACTIVE_FILE)
        logger.info("ZZZ code check finished")

    if GITHUB_PUSH:
        logger.info("Pushing code files to GitHub")
        gitpush.push(path, GITHUB_FILES)
        logger.info("Code files pushed to GitHub")


main()
