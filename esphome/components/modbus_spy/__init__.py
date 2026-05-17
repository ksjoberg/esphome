from __future__ import annotations

import esphome.codegen as cg
from esphome.components import modbus
import esphome.config_validation as cv
from esphome.const import CONF_ID

CODEOWNERS = ["@ksjoberg"]
AUTO_LOAD = ["modbus"]
MULTI_CONF = True

modbus_spy_ns = cg.esphome_ns.namespace("modbus_spy")
ModbusSpy = modbus_spy_ns.class_("ModbusSpy", cg.Component, modbus.ModbusDevice)

CONF_MODBUS_SPY_ID = "modbus_spy_id"

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(ModbusSpy),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(modbus.modbus_device_schema(None))
)

FINAL_VALIDATE_SCHEMA = modbus.final_validate_modbus_device("modbus_spy", role="spy")


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await modbus.register_modbus_device(var, config)
