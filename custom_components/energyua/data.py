"""Custom types for EnergyUA."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.loader import Integration

    from .api import EnergyUAApiClient
    from .coordinator import EnergyUACoordinator


type EnergyUAConfigEntry = ConfigEntry[EnergyUAData]


@dataclass
class EnergyUAData:
    """Data for the EnergyUA integration."""

    client: EnergyUAApiClient
    coordinator: EnergyUACoordinator
    integration: Integration
