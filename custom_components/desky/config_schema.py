import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.const import CONF_NAME

CONF_ENDPOINT = "endpoint"


ENDPOINT_SCHEMA = {
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_ENDPOINT): cv.string,
}
