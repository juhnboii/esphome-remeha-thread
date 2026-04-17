#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/uart/uart.h"

namespace esphome {
namespace remeha {

// Helper macro: creates protected sensor pointer + public setter for each sub-sensor
#define REMEHA_SUB_SENSOR(name)              \
 protected:                                  \
  sensor::Sensor *name##_sensor_{nullptr};   \
                                             \
 public:                                     \
  void set_##name##_sensor(sensor::Sensor *s) { this->name##_sensor_ = s; }

class RemehaComponent : public PollingComponent, public uart::UARTDevice {
 public:
  // --- Temperature sensors ---
  REMEHA_SUB_SENSOR(flow_temp)
  REMEHA_SUB_SENSOR(return_temp)
  REMEHA_SUB_SENSOR(dhw_in_temp)
  REMEHA_SUB_SENSOR(outside_temp)
  REMEHA_SUB_SENSOR(calorifier_temp)
  REMEHA_SUB_SENSOR(boiler_control_temp)
  REMEHA_SUB_SENSOR(room_temp)
  REMEHA_SUB_SENSOR(ch_setpoint)
  REMEHA_SUB_SENSOR(dhw_setpoint)
  REMEHA_SUB_SENSOR(room_temp_setpoint)
  REMEHA_SUB_SENSOR(control_temp)

  // --- Fan sensors ---
  REMEHA_SUB_SENSOR(fan_speed_setpoint)
  REMEHA_SUB_SENSOR(fan_speed)

  // --- Performance sensors ---
  REMEHA_SUB_SENSOR(ionisation_current)
  REMEHA_SUB_SENSOR(internal_setpoint)
  REMEHA_SUB_SENSOR(available_power)
  REMEHA_SUB_SENSOR(pump_percentage)
  REMEHA_SUB_SENSOR(desired_max_power)
  REMEHA_SUB_SENSOR(actual_power)

  // --- Demand source bits (byte 43) ---
  REMEHA_SUB_SENSOR(demand_source_bit0)
  REMEHA_SUB_SENSOR(demand_source_bit1)
  REMEHA_SUB_SENSOR(demand_source_bit2)
  REMEHA_SUB_SENSOR(demand_source_bit3)
  REMEHA_SUB_SENSOR(demand_source_bit4)
  REMEHA_SUB_SENSOR(demand_source_bit5)
  REMEHA_SUB_SENSOR(demand_source_bit6)
  REMEHA_SUB_SENSOR(demand_source_bit7)

  // --- Input bits (byte 44) ---
  REMEHA_SUB_SENSOR(input_bit0)
  REMEHA_SUB_SENSOR(input_bit1)
  REMEHA_SUB_SENSOR(input_bit2)
  REMEHA_SUB_SENSOR(input_bit3)
  REMEHA_SUB_SENSOR(input_bit5)
  REMEHA_SUB_SENSOR(input_bit6)
  REMEHA_SUB_SENSOR(input_bit7)

  // --- Valve bits (byte 45) ---
  REMEHA_SUB_SENSOR(valve_bit0)
  REMEHA_SUB_SENSOR(valve_bit2)
  REMEHA_SUB_SENSOR(valve_bit3)
  REMEHA_SUB_SENSOR(valve_bit4)
  REMEHA_SUB_SENSOR(valve_bit6)

  // --- Pump bits (byte 46) ---
  REMEHA_SUB_SENSOR(pump_bit0)
  REMEHA_SUB_SENSOR(pump_bit1)
  REMEHA_SUB_SENSOR(pump_bit2)
  REMEHA_SUB_SENSOR(pump_bit4)
  REMEHA_SUB_SENSOR(pump_bit7)

  // --- Status sensors ---
  REMEHA_SUB_SENSOR(boiler_state)
  REMEHA_SUB_SENSOR(lockout)
  REMEHA_SUB_SENSOR(blocking)
  REMEHA_SUB_SENSOR(sub_state)

  // --- Miscellaneous sensors ---
  REMEHA_SUB_SENSOR(hydro_pressure)
  REMEHA_SUB_SENSOR(hru)
  REMEHA_SUB_SENSOR(dhw_flowrate)

  // --- Counter sensors ---
  REMEHA_SUB_SENSOR(hours_run_pump)
  REMEHA_SUB_SENSOR(hours_run_3way)
  REMEHA_SUB_SENSOR(hours_run_ch)
  REMEHA_SUB_SENSOR(hours_run_dhw)
  REMEHA_SUB_SENSOR(power_supply_aval_hours)
  REMEHA_SUB_SENSOR(pump_starts)
  REMEHA_SUB_SENSOR(number_of_3way_valve_cycles)
  REMEHA_SUB_SENSOR(burner_start_dhw)
  REMEHA_SUB_SENSOR(total_burner_start)
  REMEHA_SUB_SENSOR(failed_burner_start)
  REMEHA_SUB_SENSOR(number_flame_loss)

  void setup() override {}
  void update() override;
  float get_setup_priority() const override { return setup_priority::DATA; }

 protected:
  void get_sample_();
  void get_counter_();

  static float signed_float_(float value) {
    return value > 32768.0f ? value - 65536.0f : value;
  }

  // Only publishes if the sensor is configured in YAML
  static void pub_(sensor::Sensor *s, float value) {
    if (s != nullptr)
      s->publish_state(value);
  }

  bool reading_{false};
  bool read_all_{true};
  int counter_timer_{99};
};

#undef REMEHA_SUB_SENSOR

}  // namespace remeha
}  // namespace esphome
