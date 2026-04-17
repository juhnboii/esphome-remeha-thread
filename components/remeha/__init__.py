"""ESPHome external component for Remeha / De Dietrich central heating boilers.

Registers the RemehaComponent as a PollingComponent + UARTDevice.
All sensors are configured via sensor.py (platform: remeha).
"""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import uart
from esphome.const import CONF_ID

CODEOWNERS = ["@jghaanstra"]
AUTHORS = ["@jghaanstra", "Claude Sonnet 4.6"]
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["sensor"]
MULTI_CONF = False

remeha_ns = cg.esphome_ns.namespace("remeha")
RemehaComponent = remeha_ns.class_("RemehaComponent", cg.PollingComponent, uart.UARTDevice)

# Exported so sensor.py can import it
CONF_REMEHA_ID = "remeha_id"

CONFIG_SCHEMA = (
    cv.Schema({cv.GenerateID(): cv.declare_id(RemehaComponent)})
    .extend(cv.polling_component_schema("15s"))
    .extend(uart.UART_DEVICE_SCHEMA)
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
