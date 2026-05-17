#pragma once

#include "esphome/core/component.h"
#include "esphome/components/modbus/modbus.h"
#include "esphome/components/modbus/modbus_helpers.h"
#include "esphome/components/sensor/sensor.h"

#include <vector>

namespace esphome::modbus_spy {

class ModbusSpySensor;

class ModbusSpy : public Component, public modbus::ModbusDevice {
 public:
  void on_modbus_data(const std::vector<uint8_t> &data) override {}
  void on_modbus_spy_response(uint8_t function_code, uint16_t start_address, uint16_t register_count,
                               const std::vector<uint8_t> &data) override;
  void dump_config() override;

  void add_sensor(ModbusSpySensor *sensor) { this->sensors_.push_back(sensor); }

 protected:
  std::vector<ModbusSpySensor *> sensors_;
};

class ModbusSpySensor : public sensor::Sensor, public Component {
 public:
  ModbusSpySensor(uint16_t register_address, modbus::helpers::SensorValueType value_type, uint32_t bitmask)
      : register_address_(register_address), value_type_(value_type), bitmask_(bitmask) {}

  void dump_config() override;
  void try_update(uint8_t function_code, uint16_t start_address, const std::vector<uint8_t> &data);

 protected:
  uint16_t register_address_;
  modbus::helpers::SensorValueType value_type_;
  uint32_t bitmask_;
};

}  // namespace esphome::modbus_spy
