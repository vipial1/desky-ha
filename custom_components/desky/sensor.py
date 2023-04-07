from __future__ import annotations
import requests

from datetime import timedelta

from homeassistant.components.sensor import (
    SensorEntity,
    SensorStateClass,
    SensorEntityDescription,
    SensorDeviceClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import *
from homeassistant.const import (
    CONF_NAME,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)

SCAN_INTERVAL = timedelta(minutes=1)


SENSOR_DESCRIPTIONS: list[SensorEntityDescription] = [
    # wifi
    SensorEntityDescription(
        key="desky_rssi_level",
        name="RSSI Level",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        entity_registry_enabled_default=False,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entities: list[SensorEntityDescription] = []

    for description in SENSOR_DESCRIPTIONS:
        entities.append(DeskyWifiSensor(hass, entry, description))

    async_add_entities(entities)


class DeskyWifiSensor(SensorEntity):
    def __init__(self, hass, config_entry, description):
        """Initialize the sensor."""
        super().__init__()
        self.hass = hass
        self.entity_description = description
        self._config_name = config_entry.data.get(CONF_NAME, "Default Name")
        self._endpoint = config_entry.data.get(CONF_ENDPOINT)
        self._attr_should_poll = True
        self._attr_unique_id = f"{self._config_name}_rssi_level"
        self.entity_description.key = self._attr_unique_id
        self._attr_name = description.name
        self._attr_extra_state_attributes = {}
        self._attr_device_info = {"identifiers": {(SERIAL_ID_KEY, self._config_name)}}

    async def async_update(self):
        info = await self.hass.async_add_executor_job(self._sync_get_info)
        self._attr_native_value = info["signal"]
        self._attr_extra_state_attributes["Status"] = info["status"].capitalize()
        self._attr_extra_state_attributes["SSID"] = info["ssid"]

    def _sync_get_info(self):
        return_value = requests.get(url=self._endpoint + "/api/info", timeout=10)
        return return_value.json()
