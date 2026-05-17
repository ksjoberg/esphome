from __future__ import annotations

import esphome.codegen as cg
from esphome.components import sensor
from esphome.components.modbus.helpers import SENSOR_VALUE_TYPE
import esphome.config_validation as cv
from esphome.const import CONF_ID

from .. import CONF_MODBUS_SPY_ID, ModbusSpy, modbus_spy_ns

DEPENDENCIES = ["modbus_spy"]

CONF_REGISTER_ADDRESS = "register_address"
CONF_VALUE_TYPE = "value_type"
CONF_BITMASK = "bitmask"

ModbusSpySensor = modbus_spy_ns.class_("ModbusSpySensor", sensor.Sensor, cg.Component)

CONFIG_SCHEMA = (
    sensor.sensor_schema(ModbusSpySensor)
    .extend(cv.COMPONENT_SCHEMA)
    .extend(
        {
            cv.GenerateID(CONF_MODBUS_SPY_ID): cv.use_id(ModbusSpy),
            cv.Required(CONF_REGISTER_ADDRESS): cv.hex_uint16_t,
            cv.Optional(CONF_VALUE_TYPE, default="U_WORD"): cv.enum(SENSOR_VALUE_TYPE),
            cv.Optional(CONF_BITMASK, default=0xFFFFFFFF): cv.hex_uint32_t,
        }
    )
)


async def to_code(config):
    var = cg.new_Pvariable(
        config[CONF_ID],
        config[CONF_REGISTER_ADDRESS],
        config[CONF_VALUE_TYPE],
        config[CONF_BITMASK],
    )
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)
    paren = await cg.get_variable(config[CONF_MODBUS_SPY_ID])
    cg.add(paren.add_sensor(var))
