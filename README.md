# ESPHome Remeha / Dietrich over Thread
ESPHome over Thread for Remeha / Dietrich central heating boilers
Native ESPHome external component for reading out the values of Remeha / De Dietrich central heating boilers.

Based on [jghaanstra/esphome-remeha](https://github.com/jghaanstra/esphome-remeha), rewritten to be used on Thread instead of WiFi

## Background

| ESPHome version | Status |
|---|---|
| ≤ 2025.1 | `platform: custom` + `includes:` works |
| 2025.2 | `platform: custom` removed; workaround via [robertklep/esphome-custom-component](https://github.com/robertklep/esphome-custom-component) |
| 2026.3+ | The workaround no longer works either; a native external component is required |

This repository solves the problem structurally: the logic has been converted to a proper ESPHome component with Python code generation.

## Requirements

- ESPHome 2025.2 or higher
- ESP32 (ESP32-C5, ESP32-C6, or ESP32-H2 because they have Thread radio chip)
- UART connection to the boiler at 9600 baud, 8N1

## Connection schema
```
 Heater Board from top       ESP8266
    4P4C RJ connector
    
       +---------+
GND 4  ---       +--+        GND (GND)
TXD 3  ---          |        RX (GPIO13 / D7)
RXD 2  ---          |        TX (GPIO15 / D8)
5V  1  ---       +--+        5V (VIN)
       +---------+
```


## Installation

### 1. Add the external component to your YAML

```yaml
external_components:
  - source: github://juhnboii/esphome-remeha-thread
    components: [remeha]
```

### 2. Define the UART bus

```yaml
uart:
  id: uart_bus
  baud_rate: 9600
  tx_pin: GPIO15
  rx_pin: GPIO13
  stop_bits: 1
```

### 3. Add the boiler hub

```yaml
remeha:
  id: remeha_component
  uart_id: uart_bus
  update_interval: 15s    # optional, default 15s
```

### 4. Configure sensors

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

## Migrating from the old custom component configuration

1. Remove `includes: [cv-ketel.h]` from the `esphome:` section
2. Remove the `external_components` entry for `robertklep/esphome-custom-component`
3. Remove the `platform: custom` sensor block with the lambda
4. Add the new `remeha:` hub and `platform: remeha` sensors as described above

## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).

This is a full rewrite of the original custom component as a native ESPHome external component. The protocol knowledge (command bytes, data offsets, scaling factors) is derived from the original work by kakaki. GPL-3.0 is used to ensure any derivative work remains open source.

## Credits

Original code: [jghaanstra/esphome-remeha](https://github.com/jghaanstra/esphome-remeha)
