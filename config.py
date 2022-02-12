import logging
import os

from domain.graph import Graph

REST_PORT = os.environ.get(
    "REST_PORT",
    8081
)

if REST_PORT is None:
    raise ValueError("REST_PORT has to be provided.")

SECURITY_TOKEN = os.environ.get("SECURITY_TOKEN", None)

if SECURITY_TOKEN is None:
    raise ValueError("SECURITY_TOKEN has to be provided.")

TOKEN_TYPE = os.environ.get("TOKEN_TYPE", "Bearer")

REST_PORT = int(REST_PORT)

data = []
DATABASE = Graph(data)

LOGGER = logging.getLogger("REESYNC-API")
LOGGER.setLevel(logging.DEBUG)

stdout_logger = logging.StreamHandler()
stdout_logger.setFormatter(
    logging.Formatter(
        '[%(name)s:%(filename)s:%(lineno)d] - [%(process)d] - %(asctime)s - %(levelname)s - %(message)s'
    )
)

LOGGER.addHandler(stdout_logger)
