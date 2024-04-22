"""Utility to load data into the database."""

import argparse
import logging
from pymongo import MongoClient, timeout
import os


# Logger definition -------------------------------------------------
logger = logging.getLogger(__name__)
format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


# Script arguments definition ---------------------------------------
parser = argparse.ArgumentParser(
    prog="PROG",
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog="See '<command> --help' to read about a specific sub-command.",
)
parser.add_argument(
    *["-v", "--verbosity"],
    help="Sets the logging level (default: %(default)s)",
    type=str,
    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default="INFO",
)
parser.add_argument(
    "--username",
    help="Username for connecting to the database (default: %(default)s)",
    type=str,
    default=os.getenv("APP_DATABASE_USERNAME", "user1"),
)
parser.add_argument(
    "--password_file",
    help="Secret file with database password (default: %(default)s)",
    type=str,
    default="sandbox/secrets/app_database_password",
)
parser.add_argument(
    "--host",
    help="Database host (default: %(default)s)",
    type=str,
    default=os.getenv("APP_DATABASE_HOST", "localhost"),
)
parser.add_argument(
    "--port",
    help="Database port (default: %(default)s)",
    type=int,
    default=os.getenv("APP_DATABASE_PORT", "27017"),
)
parser.add_argument(
    "file",
    help="JSON file to load into the database",
    type=str,
)


def main(args):
    logger.info("Generating database client from environment.")
    with open(args.password_file, encoding="utf-8") as f:
        client = MongoClient(
            username=args.username,
            password=f.read().strip(),
            host=args.host,
            port=args.port,
        )

    logger.info("Connecting to database %s", client)
    with timeout(seconds=3):  # Check the connection
        server_info = client.server_info()
        logger.debug("Server info: %s", server_info)

    logger.info("Loading data from %s", args.file)
    raise NotImplementedError()  # TODO add code to load data


if __name__ == "__main__":
    main(parser.parse_args())
