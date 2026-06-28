from __future__ import annotations

import esphome.codegen as cg
from esphome.components import modbus
import esphome.config_validation as cv
from esphome.const import CONF_ID

CODEOWNERS = ["@ksjoberg"]
AUTO_LOAD = ["modbus"]
MULTI_CONF = True

modbus_server_spy_ns = cg.esphome_ns.namespace("modbus_server_spy")
ModbusServerSpy = modbus_server_spy_ns.class_(
    "ModbusServerSpy", cg.Component, modbus.ModbusServerSpyDevice
)

CONF_MODBUS_SERVER_SPY_ID = "modbus_server_spy_id"

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(ModbusServerSpy),
        }
    )
    .extend(cv.COMPONENT_SCHEMA)
    .extend(modbus.modbus_device_schema(None, role="server"))
)

FINAL_VALIDATE_SCHEMA = modbus.final_validate_modbus_device(
    "modbus_server_spy", role="server"
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await modbus.register_modbus_server_spy_device(var, config)
