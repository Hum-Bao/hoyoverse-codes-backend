import logging
from pathlib import Path

import genshin
import gitpush
import starrail
import zzz
from dotenv import load_dotenv


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    path = Path(__file__).parent.absolute()
    logger.info("Working directory: %s", path)

    required_files = [
        "hsr.txt",
        "hsr_exp.txt",
        "genshin.txt",
        "genshin_exp.txt",
        "zzz.txt",
        "zzz_exp.txt",
    ]
    github_files = ["hsr.txt", "genshin.txt"]
    for file in required_files:
        file_path = path / file
        if not file_path.exists():
            logger.error("Required file %s not found at %s", file, file_path)
            with file_path.open("w"):
                pass
            logger.info("Created empty file: %s", file)

    load_dotenv()
    logger.info("Environment variables loaded")

    logger.info("Starting HSR code check")
    starrail.main(path)
    logger.info("HSR code check finished")

    logger.info("Starting Genshin code check")
    genshin.main(path)
    logger.info("Genshin code check finished")

    logger.info("Starting ZZZ code check")
    zzz.main(path)
    logger.info("ZZZ code check finished")

    logger.info("Pushing code files to GitHub")
    gitpush.push(path, github_files)
    logger.info("Code files pushed to GitHub")


main()
