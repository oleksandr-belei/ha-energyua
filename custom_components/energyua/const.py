"""Constants for EnergyUA integration."""

from datetime import timedelta
from logging import Logger, getLogger
from typing import Final

LOGGER: Logger = getLogger(__package__)

DOMAIN: Final = "energyua"

CONF_REGION: Final = "region"
CONF_GROUP: Final = "group"

STATE_NORMAL: Final = "normal"
STATE_OUTAGE: Final = "outage"

UPDATE_INTERVAL: Final = timedelta(minutes=15)
TIMEFRAME_TO_CHECK: Final = timedelta(hours=24)

ATTRIBUTION: Final = "Data provided by https://energy-ua.info"
