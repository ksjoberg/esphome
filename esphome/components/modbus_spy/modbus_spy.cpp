#include "modbus_spy.h"
#include "esphome/core/helpers.h"
#include "esphome/core/log.h"

namespace esphome::modbus_spy {

static const char *const TAG = "modbus_spy";

void ModbusSpy::on_modbus_spy_response(uint8_t function_code, uint16_t start_address, uint16_t register_count,
                                        const std::vector<uint8_t> &data) {
  ESP_LOGD(TAG, "Response FC=0x%02X unit=%" PRIu8 " start=0x%04X count=%" PRIu16 " bytes=%zu", function_code,
           this->address_, start_address, register_count, data.size());
  for (auto *sensor : this->sensors_) {
    sensor->try_update(function_code, start_address, data);
  }
}

void ModbusSpy::dump_config() {
  ESP_LOGCONFIG(TAG, "Modbus Spy:");
  ESP_LOGCONFIG(TAG, "  Address: 0x%02X", this->address_);
}

void ModbusSpySensor::try_update(uint8_t function_code, uint16_t start_address, const std::vector<uint8_t> &data) {
  // Only handle read register responses (FC 01-04)
  if (function_code > 0x04)
    return;
  // Register must be within the response range
  if (this->register_address_ < start_address)
    return;
  uint16_t reg_offset = this->register_address_ - start_address;
  uint8_t byte_offset = reg_offset * 2;

  int64_t raw =
      modbus::helpers::payload_to_number(data, this->value_type_, byte_offset, this->bitmask_);

  float value;
  if (modbus::helpers::value_type_is_float(this->value_type_)) {
    value = bit_cast<float>(static_cast<uint32_t>(raw));
  } else {
    value = static_cast<float>(raw);
  }

  ESP_LOGD(TAG, "  Register 0x%04X = %f", this->register_address_, value);
  this->publish_state(value);
}

void ModbusSpySensor::dump_config() {
  LOG_SENSOR("", "Modbus Spy Sensor", this);
  ESP_LOGCONFIG(TAG, "  Register: 0x%04X", this->register_address_);
  ESP_LOGCONFIG(TAG, "  Value Type: %u", static_cast<unsigned int>(this->value_type_));
  ESP_LOGCONFIG(TAG, "  Bitmask: 0x%08" PRIX32, this->bitmask_);
}

}  // namespace esphome::modbus_spy
