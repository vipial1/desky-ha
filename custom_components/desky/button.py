from __future__ import annotations
import requests

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import *
from homeassistant.const import (
    CONF_NAME,
)

BUTTON_DESCRIPTIONS: list[ButtonEntityDescription] = [
    ButtonEntityDescription(
        key="1",
        name="Memory 1",
        icon="mdi:gesture-tap-button",
    ),
    ButtonEntityDescription(
        key="2",
        name="Memory 2",
        icon="mdi:gesture-tap-button",
    ),
    ButtonEntityDescription(
        key="3",
        name="Memory 3",
        icon="mdi:gesture-tap-button",
    ),
    ButtonEntityDescription(
        key="4",
        name="Memory 4",
        icon="mdi:gesture-tap-button",
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entities: list[ButtonEntity] = []

    for description in BUTTON_DESCRIPTIONS:
        entities.append(AutonomousTableButton(hass, entry, description))

    async_add_entities(entities)


class AutonomousTableButton(ButtonEntity):
    def __init__(self, hass, config_entry, description):
        """Initialize the button."""
        super().__init__()
        self.hass = hass
        self.entity_description = description
        self._config_name = config_entry.data.get(CONF_NAME, "Default Name")
        self._endpoint = config_entry.data.get(CONF_ENDPOINT)
        self._attr_should_poll = True
        self._button_id = description.key
        self._attr_unique_id = f"{self._config_name}_button_{self._button_id}"
        self._attr_name = description.name
        self._attr_device_info = {"identifiers": {(SERIAL_ID_KEY, self._config_name)}}

    async def async_press(self) -> None:
        await self.hass.async_add_executor_job(self._sync_post_mem)

    def _sync_post_mem(self):
        requests.post(
            url=self._endpoint + "/api/mem",
            data=f'{{"button" : "{self._button_id}"}}',
            timeout=10,
        )
