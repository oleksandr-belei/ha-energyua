"""Adds config flow for EnergyUA."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import selector
from slugify import slugify

from .api import (
    EnergyUAApiClient,
    EnergyUAApiClientCommunicationError,
    EnergyUAApiClientError,
)
from .const import CONF_GROUP, CONF_REGION, DOMAIN, LOGGER


class EnergyUAFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for EnergyUA."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize config flow."""
        self.client = EnergyUAApiClient()
        self.data: dict[str, Any] = {}

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        if user_input is not None:
            LOGGER.debug("Region selected: %s", user_input)
            self.data.update(user_input)
            self.client.region = self.data[CONF_REGION]
            return await self.async_step_group()

        _errors = {}

        try:
            await self.client.fetch_regions()
        except EnergyUAApiClientCommunicationError as exception:
            LOGGER.error(exception)
            _errors["base"] = "connection"
        except EnergyUAApiClientError as exception:
            LOGGER.exception(exception)
            _errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=_build_region_schema(client=self.client),
            errors=_errors,
            last_step=False,
        )

    async def async_step_group(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the group step."""
        if user_input is not None:
            LOGGER.debug("Group selected: %s", user_input)
            self.data.update(user_input)
            self.client.group = self.data[CONF_GROUP]

            unique_id = f"{self.data[CONF_REGION]}_{self.data[CONF_GROUP]}"
            unique_id = slugify(unique_id)

            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            region_label = self.client.get_region_label()
            group_label = self.client.get_group_label()

            title = f"{region_label} {group_label}"

            return self.async_create_entry(title=title, data=self.data)

        _errors = {}

        try:
            await self.client.fetch_groups()
        except EnergyUAApiClientCommunicationError as exception:
            LOGGER.error(exception)
            _errors["base"] = "connection"
        except EnergyUAApiClientError as exception:
            LOGGER.exception(exception)
            _errors["base"] = "unknown"

        return self.async_show_form(
            step_id="group",
            data_schema=_build_group_schema(client=self.client),
            errors=_errors,
            last_step=True,
        )


def _build_region_schema(
    client: EnergyUAApiClient,
) -> vol.Schema:
    """Build the schema for the region selection step."""
    regions = client.get_regions()

    region_options: list[selector.SelectOptionDict] = [
        selector.SelectOptionDict(
            value=region["value"],
            label=region["label"],
        )
        for region in regions
    ]

    return vol.Schema(
        {
            vol.Required(
                CONF_REGION,
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=region_options,
                    translation_key="region",
                ),
            ),
        },
    )


def _build_group_schema(
    client: EnergyUAApiClient,
) -> vol.Schema:
    """Build the schema for the group selection step."""
    groups = client.get_groups()

    group_options: list[selector.SelectOptionDict] = [
        selector.SelectOptionDict(
            value=group["value"],
            label=group["label"],
        )
        for group in groups
    ]

    return vol.Schema(
        {
            vol.Required(
                CONF_GROUP,
            ): selector.SelectSelector(
                selector.SelectSelectorConfig(
                    options=group_options,
                    translation_key="group",
                ),
            ),
        },
    )
