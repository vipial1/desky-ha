from homeassistant import config_entries
from homeassistant.const import CONF_NAME
import uuid
import logging
from .config_schema import ENDPOINT_SCHEMA
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register("desky-ha")
class DeskyHAFlowHandler(config_entries.ConfigFlow, domain="desky-ha"):
    """Handle a config flow."""

    VERSION = 1

    def __init__(self):
        """Initialize."""
        self._errors = {}
        self._data = {}
        self._config_complete = False
        self._unique_id = str(uuid.uuid4())

    async def async_step_user(self, user_input=None):
        self._errors = {}

        _LOGGER.debug("user_input= %s", user_input)
        if user_input:
            self._data.update(user_input)
            return self.async_create_entry(
                title=user_input.get(CONF_NAME), data=self._data
            )

        return await self._show_config_form_user()

    async def _show_config_form_user(self):
        """Show form for config flow"""
        _LOGGER.info("Show endpoint form")
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(ENDPOINT_SCHEMA),
            errors=self._errors,
        )
