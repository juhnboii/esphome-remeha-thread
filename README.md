# ESPHome Remeha / Dietrich over Thread
ESPHome over Thread for Remeha / Dietrich central heating boilers

Native ESPHome external component for reading out the values of Remeha / De Dietrich central heating boilers.
Based on [jghaanstra/esphome-remeha](https://github.com/jghaanstra/esphome-remeha), rewritten to be used on Thread instead of WiFi

## Requirements

- ESPHome 2025.2 or higher
- Waveshare ESP32-C6-WROOM-1-NX (because it has a Thread radio chip onboard)
- Adafruit RS232 Pal (TTL-to-RS232 converter, since the ESP32-C6 only supports TTL)
- UART connection to the boiler at 9600 baud, 8N1

## Connection schema
```
Will be posted once known
```

## Installation

### 1. Add you board model (e.g. ESP32-C6-WROOM-1-NX)

```yaml
esp32:
  board: esp32-c6-devkitc-1
  variant: esp32c6
  framework:
    type: esp-idf
```

### 2. Add your TLV

HomeAssistant:
You can find your Thread TLV at Integrations > Thread > (gear icon) > Preferred Network > (info icon) > in the bottom Active Dataset TLVs.
Copy this long string value, this is your TLV.

```yaml
openthread:
  device_type: FTD
  tlv: "your-tlv-here"
```

### 3. Add a (random) API encryption key

```yaml
api:
  encryption:
    key: "your-random-key-here"
```

### 4. Add a (random) OTA password

```yaml
ota:
  platform: esphome
  password: "your-random-password-here"
```

### 5. Add the external component

```yaml
external_components:
  - source: github://juhnboii/esphome-remeha-thread
    components: [remeha]
```

### 6. Define the UART bus

```yaml
uart:
  id: uart_bus
  baud_rate: 9600
  tx_pin: GPIO6
  rx_pin: GPIO7
  stop_bits: 1
```

### 7. Add the boiler hub

```yaml
remeha:
  id: remeha_component
  uart_id: uart_bus
  update_interval: 15s    # optional, default 15s
```

### 8. Configure sensors

All sensors are optional. Only add the sensors you need:

```yaml
sensor:
  - platform: remeha
    remeha_id: remeha_component
    flow_temp:
      name: "Boiler flow temperature"
    return_temp:
      name: "Boiler return temperature"
    boiler_state:
      name: "Boiler state (numeric)"
    # ... see example-cv-ketel.yaml for all available sensors
```

See [example-cv-ketel.yaml](example-cv-ketel.yaml) for a complete configuration including text sensors for human-readable state descriptions.

## Available sensors

### Temperatures
| Key | Unit | Description |
|---|---|---|
| `flow_temp` | °C | Flow temperature |
| `return_temp` | °C | Return temperature |
| `dhw_in_temp` | °C | DHW inlet temperature |
| `outside_temp` | °C | Outside temperature |
| `calorifier_temp` | °C | Calorifier temperature |
| `boiler_control_temp` | °C | Internal control temperature |
| `room_temp` | °C | Room temperature |
| `ch_setpoint` | °C | CH setpoint |
| `dhw_setpoint` | °C | DHW setpoint |
| `room_temp_setpoint` | °C | Room temperature setpoint |
| `control_temp` | °C | Control temperature |

### Fan & power
| Key | Unit | Description |
|---|---|---|
| `fan_speed_setpoint` | rpm | Fan speed setpoint |
| `fan_speed` | rpm | Actual fan speed |
| `ionisation_current` | μA | Ionisation current |
| `internal_setpoint` | % | Internal setpoint |
| `available_power` | % | Available power |
| `pump_percentage` | % | Pump percentage |
| `desired_max_power` | % | Desired maximum power |
| `actual_power` | % | Actual power |

### Status
| Key | Description |
|---|---|
| `boiler_state` | Boiler state (0–17, see example YAML for text mapping) |
| `sub_state` | Sub-state (see example YAML) |
| `lockout` | Lockout code |
| `blocking` | Blocking code |

### Miscellaneous
| Key | Unit | Description |
|---|---|---|
| `hydro_pressure` | bar | Water pressure |
| `dhw_flowrate` | L/min | DHW flow rate |
| `hru` | — | HRU bit 1 |
| `demand_source_bit0`–`bit7` | — | Heat demand source bits |
| `input_bit0/1/2/3/5/6/7` | — | Input status bits |
| `valve_bit0/2/3/4/6` | — | Valve status bits |
| `pump_bit0/1/2/4/7` | — | Pump status bits |

### Counters
| Key | Unit | Description |
|---|---|---|
| `hours_run_pump` | h | Pump operating hours |
| `hours_run_3way` | h | 3-way valve operating hours |
| `hours_run_ch` | h | CH operating hours |
| `hours_run_dhw` | h | DHW operating hours |
| `power_supply_aval_hours` | h | Power supply available hours |
| `pump_starts` | — | Pump starts |
| `number_of_3way_valve_cycles` | — | 3-way valve cycles |
| `burner_start_dhw` | — | Burner starts DHW |
| `total_burner_start` | — | Total burner starts |
| `failed_burner_start` | — | Failed burner starts |
| `number_flame_loss` | — | Flame loss count |

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

This is a full rewrite of the original custom component as a native ESPHome external component. The protocol knowledge (command bytes, data offsets, scaling factors) is derived from the original work by kakaki. GPL-3.0 is used to ensure any derivative work remains open source.

## Credits

Original code: [jghaanstra/esphome-remeha](https://github.com/jghaanstra/esphome-remeha)
