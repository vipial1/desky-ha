"""The Desky integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import *
from homeassistant.const import CONF_NAME, Platform
from homeassistant.helpers import device_registry as dr

PLATFORMS = [
    Platform.NUMBER,
    Platform.BUTTON,
    Platform.SENSOR,
]


async def async_setup(hass: HomeAssistant, config) -> bool:
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data.pop(PLATFORM, None)

    return unload_ok


async def async_setup_entry(hass, config_entry):
    register_device(hass, config_entry, config_entry.data.get(CONF_NAME))
    hass.config_entries.async_setup_platforms(config_entry, PLATFORMS)

    return True


async def update_listener(hass, config_entry):
    """Handle options update."""
    await hass.config_entries.async_reload(config_entry.entry_id)


def register_device(hass, config_entry, device_name):
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=config_entry.entry_id,
        identifiers={(SERIAL_ID_KEY, device_name)},
        name=device_name,
    )
