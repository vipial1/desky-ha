import logging
import requests

from homeassistant.helpers.reload import async_setup_reload_service
from homeassistant.helpers.restore_state import RestoreEntity
from datetime import timedelta
from .const import *
from homeassistant.const import (
    CONF_NAME,
)

from homeassistant.components.number import (
    NumberMode,
    NumberEntity,
    NumberEntityDescription,
)
from .const import CONF_ENDPOINT


_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=1)


async def async_create_entities(hass, config_entry, async_add_devices):
    await async_setup_reload_service(hass, DOMAIN, PLATFORM)
    async_add_devices(
        [
            AutonomousTableHeight(hass, config_entry),
        ],
        update_before_add=True,
    )


async def async_setup_entry(hass, config_entry, async_add_devices):
    await async_create_entities(hass, config_entry, async_add_devices)


class AutonomousTableHeight(NumberEntity, RestoreEntity):
    """AutonomousTableHeight"""

    def __init__(self, hass, config_entry):
        """Initialize the sensor."""
        super().__init__()
        self.hass = hass
        self._config_name = config_entry.data.get(CONF_NAME, "Default Name")
        self._endpoint = config_entry.data.get(CONF_ENDPOINT)
        self._attr_should_poll = True
        self._attr_unique_id = f"{self._config_name}_table_height"
        self._attr_name = f"{self._config_name} table height"
        self._attr_extra_state_attributes = {}
        self._attr_native_unit_of_measurement = "cm"
        self.entity_description = DefaultNumberEntityDescription()
        self._attr_mode: NumberMode.SLIDER
        self._attr_device_info = {"identifiers": {(SERIAL_ID_KEY, self._config_name)}}

    async def async_update(self):
        self._attr_native_value = await self.hass.async_add_executor_job(
            self._sync_get_height
        )
        info = await self.hass.async_add_executor_job(self._sync_get_info)
        self._attr_available = info["status"] == "connected"

    def set_native_value(self, value: float) -> None:
        int_value = int(value)
        requests.post(
            url=self._endpoint + "/api/height",
            data=f'{{"height" : "{int_value}"}}',
            timeout=10,
        )

    def _sync_get_height(self):
        return_value = requests.get(url=self._endpoint + "/api/height", timeout=10)
        return return_value.json()["height"]

    def _sync_get_info(self):
        return_value = requests.get(url=self._endpoint + "/api/info", timeout=10)
        return return_value.json()


class DefaultNumberEntityDescription(NumberEntityDescription):

    def __init__(self):
        super().__init__(
            key="table_position",
            name="Table Position",
            icon="mdi:table-furniture",
            native_min_value=float(75),
            native_max_value=float(123),
            native_step=float(1),
            unit_of_measurement="cm",
        )
