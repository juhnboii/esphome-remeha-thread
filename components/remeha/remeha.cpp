#include "remeha.h"
#include "esphome/core/log.h"
#include <cstring>

namespace esphome {
namespace remeha {

static const char *const TAG = "remeha";

// UART commands to the boiler (protocol: STX, dest, src, len_hi, len_lo, func_hi, func_lo, crc_hi, crc_lo, ETX)
static const uint8_t SAMPLE_CMD[]   = {0x02, 0xFE, 0x01, 0x05, 0x08, 0x02, 0x01, 0x69, 0xAB, 0x03};
static const uint8_t COUNTER1_CMD[] = {0x02, 0xFE, 0x00, 0x05, 0x08, 0x10, 0x1C, 0x98, 0xC2, 0x03};
static const uint8_t COUNTER2_CMD[] = {0x02, 0xFE, 0x00, 0x05, 0x08, 0x10, 0x1D, 0x59, 0x02, 0x03};

// ---------------------------------------------------------------------------
// update() — called every update_interval by the ESPHome scheduler
// ---------------------------------------------------------------------------
void RemehaComponent::update() {
  if (this->reading_)
    return;

  this->reading_ = true;
  this->counter_timer_++;
  ESP_LOGD(TAG, "update() called, counter_timer=%d", this->counter_timer_);

  if (this->counter_timer_ >= 8) {
    this->counter_timer_ = 0;
    this->get_counter_();
  } else {
    this->get_sample_();
  }

  this->reading_ = false;
}

// ---------------------------------------------------------------------------
// Helper: drain UART buffer into 'buf' (max 'max_len' bytes)
// ---------------------------------------------------------------------------
static int read_response(uart::UARTDevice *dev, uint8_t *buf, int max_len) {
  int n = 0;
  uint8_t b;
  while (dev->available() && n < max_len) {
    dev->read_byte(&b);
    buf[n++] = b;
  }
  return n;
}

// ---------------------------------------------------------------------------
// get_sample_() — requests measurement data (temperatures, power, bits, status)
// ---------------------------------------------------------------------------
void RemehaComponent::get_sample_() {
  uint8_t data[80];
  memset(data, 0, sizeof(data));

  this->write_array(SAMPLE_CMD, sizeof(SAMPLE_CMD));
  delay(400);  // Wait for boiler response (at 9600 baud ~83 ms for 80 bytes)

  int n = read_response(this, data, sizeof(data));

  // Debug: log raw data as hex string
  char hex[161] = {};
  for (int i = 0; i < n && i < 80; i++)
    snprintf(&hex[i * 2], 3, "%02X", data[i]);
  ESP_LOGD(TAG, "Sample (%d bytes): %s", n, hex);

  // Validate response header: STX=0x02, type=0x01, src=0xFE
  if (n < 62 || data[0] != 0x02 || data[1] != 0x01 || data[2] != 0xFE) {
    ESP_LOGW(TAG, "Invalid sample response: %02X %02X %02X (n=%d)", data[0], data[1], data[2], n);
    return;
  }

  // --- Always-published sensors (every cycle) ---
  // Little-endian 16-bit, scale factor 0.01 → degrees Celsius
  pub_(flow_temp_sensor_,         signed_float_((data[8]  * 256) + data[7])  * 0.01f);
  pub_(return_temp_sensor_,       signed_float_((data[10] * 256) + data[9])  * 0.01f);
  pub_(dhw_in_temp_sensor_,       signed_float_((data[12] * 256) + data[11]) * 0.01f);
  pub_(outside_temp_sensor_,      signed_float_((data[14] * 256) + data[13]) * 0.01f);
  pub_(calorifier_temp_sensor_,   signed_float_((data[16] * 256) + data[15]) * 0.01f);
  pub_(boiler_control_temp_sensor_, signed_float_((data[20] * 256) + data[19]) * 0.01f);
  pub_(room_temp_sensor_,         signed_float_((data[22] * 256) + data[21]) * 0.01f);
  pub_(ch_setpoint_sensor_,       signed_float_((data[24] * 256) + data[23]) * 0.01f);
  pub_(dhw_setpoint_sensor_,      signed_float_((data[26] * 256) + data[25]) * 0.01f);
  pub_(room_temp_setpoint_sensor_, signed_float_((data[28] * 256) + data[27]) * 0.01f);

  // --- Alternating sensors (every 2nd cycle, to spread API load) ---
  if (this->read_all_) {
    pub_(fan_speed_setpoint_sensor_, signed_float_((data[30] * 256) + data[29]));
    pub_(fan_speed_sensor_,          signed_float_((data[32] * 256) + data[31]));
    pub_(ionisation_current_sensor_, data[33] * 0.1f);
    pub_(internal_setpoint_sensor_,  signed_float_((data[35] * 256) + data[34]) * 0.01f);
    pub_(available_power_sensor_,    data[36]);
    pub_(pump_percentage_sensor_,    data[37]);
    pub_(desired_max_power_sensor_,  data[39]);
    pub_(actual_power_sensor_,       data[40]);

    uint8_t bits = data[43];  // Demand source
    pub_(demand_source_bit0_sensor_, (bits >> 0) & 0x01);
    pub_(demand_source_bit1_sensor_, (bits >> 1) & 0x01);
    pub_(demand_source_bit2_sensor_, (bits >> 2) & 0x01);
    pub_(demand_source_bit3_sensor_, (bits >> 3) & 0x01);
    pub_(demand_source_bit4_sensor_, (bits >> 4) & 0x01);
    pub_(demand_source_bit5_sensor_, (bits >> 5) & 0x01);
    pub_(demand_source_bit6_sensor_, (bits >> 6) & 0x01);
    pub_(demand_source_bit7_sensor_, (bits >> 7) & 0x01);

    bits = data[44];  // Input status
    pub_(input_bit0_sensor_, (bits >> 0) & 0x01);
    pub_(input_bit1_sensor_, (bits >> 1) & 0x01);
    pub_(input_bit2_sensor_, (bits >> 2) & 0x01);
    pub_(input_bit3_sensor_, (bits >> 3) & 0x01);
    pub_(input_bit5_sensor_, (bits >> 5) & 0x01);
    pub_(input_bit6_sensor_, (bits >> 6) & 0x01);
    pub_(input_bit7_sensor_, (bits >> 7) & 0x01);

    bits = data[45];  // Valve status
    pub_(valve_bit0_sensor_, (bits >> 0) & 0x01);
    pub_(valve_bit2_sensor_, (bits >> 2) & 0x01);
    pub_(valve_bit3_sensor_, (bits >> 3) & 0x01);
    pub_(valve_bit4_sensor_, (bits >> 4) & 0x01);
    pub_(valve_bit6_sensor_, (bits >> 6) & 0x01);

    bits = data[46];  // Pump status
    pub_(pump_bit0_sensor_, (bits >> 0) & 0x01);
    pub_(pump_bit1_sensor_, (bits >> 1) & 0x01);
    pub_(pump_bit2_sensor_, (bits >> 2) & 0x01);
    pub_(pump_bit4_sensor_, (bits >> 4) & 0x01);
    pub_(pump_bit7_sensor_, (bits >> 7) & 0x01);
  }

  pub_(boiler_state_sensor_, data[47]);
  pub_(lockout_sensor_,      data[48]);
  pub_(blocking_sensor_,     data[49]);
  pub_(sub_state_sensor_,    data[50]);

  if (this->read_all_) {
    pub_(hydro_pressure_sensor_, data[56]);

    uint8_t bits = data[57];
    pub_(hru_sensor_, (bits >> 1) & 0x01);

    pub_(control_temp_sensor_, signed_float_((data[59] * 256) + data[58]) * 0.01f);
    pub_(dhw_flowrate_sensor_, signed_float_((data[61] * 256) + data[60]) * 0.01f);
  }

  this->read_all_ = !this->read_all_;
}

// ---------------------------------------------------------------------------
// get_counter_() — requests counter data (run hours, starts, etc.)
// ---------------------------------------------------------------------------
void RemehaComponent::get_counter_() {
  uint8_t data[28];
  char hex[57] = {};

  // --- Counter 1 ---
  memset(data, 0, sizeof(data));
  this->write_array(COUNTER1_CMD, sizeof(COUNTER1_CMD));
  delay(150);

  int n = read_response(this, data, sizeof(data));
  for (int i = 0; i < n; i++)
    snprintf(&hex[i * 2], 3, "%02X", data[i]);
  ESP_LOGD(TAG, "Counter1 (%d bytes): %s", n, hex);

  // Response: big-endian 16-bit integers
  if (n >= 23 && data[0] == 0x02 && data[1] == 0x00 && data[2] == 0xFE) {
    pub_(hours_run_pump_sensor_,            ((data[7]  * 256) + data[8])  * 2);
    pub_(hours_run_3way_sensor_,            ((data[9]  * 256) + data[10]) * 2);
    pub_(hours_run_ch_sensor_,              ((data[11] * 256) + data[12]) * 2);
    pub_(hours_run_dhw_sensor_,              (data[13] * 256) + data[14]);
    pub_(power_supply_aval_hours_sensor_,   ((data[15] * 256) + data[16]) * 2);
    pub_(pump_starts_sensor_,               ((data[17] * 256) + data[18]) * 8);
    pub_(number_of_3way_valve_cycles_sensor_, ((data[19] * 256) + data[20]) * 8);
    pub_(burner_start_dhw_sensor_,          ((data[21] * 256) + data[22]) * 8);
  } else {
    ESP_LOGW(TAG, "Invalid counter1 response: %02X %02X %02X (n=%d)", data[0], data[1], data[2], n);
  }

  // --- Counter 2 ---
  memset(data, 0, sizeof(data));
  this->write_array(COUNTER2_CMD, sizeof(COUNTER2_CMD));
  delay(150);

  n = read_response(this, data, sizeof(data));
  for (int i = 0; i < n; i++)
    snprintf(&hex[i * 2], 3, "%02X", data[i]);
  ESP_LOGD(TAG, "Counter2 (%d bytes): %s", n, hex);

  if (n >= 13 && data[0] == 0x02 && data[1] == 0x00 && data[2] == 0xFE) {
    pub_(total_burner_start_sensor_,  ((data[7]  * 256) + data[8])  * 8);
    pub_(failed_burner_start_sensor_,  (data[9]  * 256) + data[10]);
    pub_(number_flame_loss_sensor_,    (data[11] * 256) + data[12]);
  } else {
    ESP_LOGW(TAG, "Invalid counter2 response: %02X %02X %02X (n=%d)", data[0], data[1], data[2], n);
  }
}

}  // namespace remeha
}  // namespace esphome
