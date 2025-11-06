"""Custom integration to integrate EnergyUA with Home Assistant."""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import Platform
from homeassistant.loader import async_get_loaded_integration

from .api import EnergyUAApiClient
from .const import CONF_GROUP, CONF_REGION, DOMAIN, LOGGER, UPDATE_INTERVAL
from .coordinator import EnergyUACoordinator
from .data import EnergyUAData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import EnergyUAConfigEntry

PLATFORMS: list[Platform] = [Platform.CALENDAR, Platform.SENSOR]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: EnergyUAConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    coordinator = EnergyUACoordinator(
        hass=hass,
        logger=LOGGER,
        name=DOMAIN,
        update_interval=UPDATE_INTERVAL,
    )
    entry.runtime_data = EnergyUAData(
        client=EnergyUAApiClient(
            region=entry.data[CONF_REGION],
            group=entry.data[CONF_GROUP],
        ),
        coordinator=coordinator,
        integration=async_get_loaded_integration(hass, entry.domain),
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: EnergyUAConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: EnergyUAConfigEntry,
) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
