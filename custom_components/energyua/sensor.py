"""Sensor platform for EnergyUA."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)

from .const import STATE_NORMAL, STATE_OUTAGE
from .entity import EnergyUAEntity

if TYPE_CHECKING:
    from collections.abc import Callable

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import EnergyUACoordinator
    from .data import EnergyUAConfigEntry


@dataclass(frozen=True, kw_only=True)
class EnergyUASensorDescription(SensorEntityDescription):
    """EnergyUA entity description."""

    val_func: Callable[[EnergyUACoordinator], Any]


ENTITY_DESCRIPTIONS = (
    EnergyUASensorDescription(
        key="electricity",
        translation_key="electricity",
        icon="mdi:transmission-tower",
        device_class=SensorDeviceClass.ENUM,
        options=[STATE_NORMAL, STATE_OUTAGE],
        val_func=lambda coordinator: coordinator.current_state,
    ),
    EnergyUASensorDescription(
        key="next_outage",
        translation_key="next_outage",
        icon="mdi:calendar-remove",
        device_class=SensorDeviceClass.TIMESTAMP,
        val_func=lambda coordinator: coordinator.next_outage,
    ),
    EnergyUASensorDescription(
        key="next_restore",
        translation_key="next_restore",
        icon="mdi:calendar-check",
        device_class=SensorDeviceClass.TIMESTAMP,
        val_func=lambda coordinator: coordinator.next_restore,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,  # noqa: ARG001 Unused function argument: `hass`
    entry: EnergyUAConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    async_add_entities(
        EnergyUASensor(
            coordinator=entry.runtime_data.coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class EnergyUASensor(EnergyUAEntity, SensorEntity):
    """EnergyUA Sensor class."""

    entity_description: EnergyUASensorDescription

    def __init__(
        self,
        coordinator: EnergyUACoordinator,
        entity_description: EnergyUASensorDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description
        self._attr_unique_id = (
            f"{coordinator.config_entry.entry_id}-{self.entity_description.key}"
        )

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        return self.entity_description.val_func(self.coordinator)
