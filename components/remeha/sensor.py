"""Sensor platform for the Remeha / De Dietrich boiler component.

Usage in YAML:
  sensor:
    - platform: remeha
      remeha_id: remeha_component
      flow_temp:
        name: "Boiler flow temperature"
      ...
"""
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import (
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_PRESSURE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_CELSIUS,
    UNIT_PERCENT,
)
from . import RemehaComponent, CONF_REMEHA_ID

# ---------------------------------------------------------------------------
# Units without an ESPHome constant
# ---------------------------------------------------------------------------
UNIT_HOURS = "h"
UNIT_RPM = "rpm"
UNIT_MICROAMPERE = "μA"
UNIT_LITERS_PER_MIN = "L/min"
UNIT_BAR = "bar"

# ---------------------------------------------------------------------------
# CONFIG_SCHEMA — all sensors are optional
# ---------------------------------------------------------------------------
CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(CONF_REMEHA_ID): cv.use_id(RemehaComponent),

        # --- Temperature measurement ---
        cv.Optional("flow_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("return_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("dhw_in_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("outside_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("calorifier_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("boiler_control_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("room_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("ch_setpoint"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("dhw_setpoint"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("room_temp_setpoint"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("control_temp"): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),

        # --- Fan ---
        cv.Optional("fan_speed_setpoint"): sensor.sensor_schema(
            unit_of_measurement=UNIT_RPM,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("fan_speed"): sensor.sensor_schema(
            unit_of_measurement=UNIT_RPM,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),

        # --- Performance ---
        cv.Optional("ionisation_current"): sensor.sensor_schema(
            unit_of_measurement=UNIT_MICROAMPERE,
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("internal_setpoint"): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("available_power"): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("pump_percentage"): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("desired_max_power"): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("actual_power"): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),

        # --- Status ---
        cv.Optional("boiler_state"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("lockout"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("blocking"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("sub_state"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),

        # --- Pressure and flow rate ---
        cv.Optional("hydro_pressure"): sensor.sensor_schema(
            unit_of_measurement=UNIT_BAR,
            accuracy_decimals=2,
            device_class=DEVICE_CLASS_PRESSURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("dhw_flowrate"): sensor.sensor_schema(
            unit_of_measurement=UNIT_LITERS_PER_MIN,
            accuracy_decimals=1,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional("hru"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_MEASUREMENT,
        ),

        # --- Demand source bits ---
        cv.Optional("demand_source_bit0"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("demand_source_bit1"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("demand_source_bit2"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("demand_source_bit3"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("demand_source_bit4"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("demand_source_bit5"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("demand_source_bit6"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("demand_source_bit7"): sensor.sensor_schema(accuracy_decimals=0),

        # --- Input bits ---
        cv.Optional("input_bit0"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("input_bit1"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("input_bit2"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("input_bit3"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("input_bit5"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("input_bit6"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("input_bit7"): sensor.sensor_schema(accuracy_decimals=0),

        # --- Valve bits ---
        cv.Optional("valve_bit0"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("valve_bit2"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("valve_bit3"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("valve_bit4"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("valve_bit6"): sensor.sensor_schema(accuracy_decimals=0),

        # --- Pump bits ---
        cv.Optional("pump_bit0"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("pump_bit1"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("pump_bit2"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("pump_bit4"): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional("pump_bit7"): sensor.sensor_schema(accuracy_decimals=0),

        # --- Counters ---
        cv.Optional("hours_run_pump"): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOURS,
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("hours_run_3way"): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOURS,
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("hours_run_ch"): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOURS,
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("hours_run_dhw"): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOURS,
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("power_supply_aval_hours"): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOURS,
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("pump_starts"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("number_of_3way_valve_cycles"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("burner_start_dhw"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("total_burner_start"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("failed_burner_start"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional("number_flame_loss"): sensor.sensor_schema(
            accuracy_decimals=0,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
    }
)


# ---------------------------------------------------------------------------
# to_code — registers each configured sensor with the hub
# ---------------------------------------------------------------------------
async def to_code(config):
    hub = await cg.get_variable(config[CONF_REMEHA_ID])

    async def reg(key, setter):
        if key in config:
            s = await sensor.new_sensor(config[key])
            cg.add(getattr(hub, setter)(s))

    # Temperature
    await reg("flow_temp",           "set_flow_temp_sensor")
    await reg("return_temp",         "set_return_temp_sensor")
    await reg("dhw_in_temp",         "set_dhw_in_temp_sensor")
    await reg("outside_temp",        "set_outside_temp_sensor")
    await reg("calorifier_temp",     "set_calorifier_temp_sensor")
    await reg("boiler_control_temp", "set_boiler_control_temp_sensor")
    await reg("room_temp",           "set_room_temp_sensor")
    await reg("ch_setpoint",         "set_ch_setpoint_sensor")
    await reg("dhw_setpoint",        "set_dhw_setpoint_sensor")
    await reg("room_temp_setpoint",  "set_room_temp_setpoint_sensor")
    await reg("control_temp",        "set_control_temp_sensor")
    # Fan
    await reg("fan_speed_setpoint",  "set_fan_speed_setpoint_sensor")
    await reg("fan_speed",           "set_fan_speed_sensor")
    # Performance
    await reg("ionisation_current",  "set_ionisation_current_sensor")
    await reg("internal_setpoint",   "set_internal_setpoint_sensor")
    await reg("available_power",     "set_available_power_sensor")
    await reg("pump_percentage",     "set_pump_percentage_sensor")
    await reg("desired_max_power",   "set_desired_max_power_sensor")
    await reg("actual_power",        "set_actual_power_sensor")
    # Status
    await reg("boiler_state",        "set_boiler_state_sensor")
    await reg("lockout",             "set_lockout_sensor")
    await reg("blocking",            "set_blocking_sensor")
    await reg("sub_state",           "set_sub_state_sensor")
    # Pressure / flow rate
    await reg("hydro_pressure",      "set_hydro_pressure_sensor")
    await reg("dhw_flowrate",        "set_dhw_flowrate_sensor")
    await reg("hru",                 "set_hru_sensor")
    # Demand source bits
    await reg("demand_source_bit0",  "set_demand_source_bit0_sensor")
    await reg("demand_source_bit1",  "set_demand_source_bit1_sensor")
    await reg("demand_source_bit2",  "set_demand_source_bit2_sensor")
    await reg("demand_source_bit3",  "set_demand_source_bit3_sensor")
    await reg("demand_source_bit4",  "set_demand_source_bit4_sensor")
    await reg("demand_source_bit5",  "set_demand_source_bit5_sensor")
    await reg("demand_source_bit6",  "set_demand_source_bit6_sensor")
    await reg("demand_source_bit7",  "set_demand_source_bit7_sensor")
    # Input bits
    await reg("input_bit0",          "set_input_bit0_sensor")
    await reg("input_bit1",          "set_input_bit1_sensor")
    await reg("input_bit2",          "set_input_bit2_sensor")
    await reg("input_bit3",          "set_input_bit3_sensor")
    await reg("input_bit5",          "set_input_bit5_sensor")
    await reg("input_bit6",          "set_input_bit6_sensor")
    await reg("input_bit7",          "set_input_bit7_sensor")
    # Valve bits
    await reg("valve_bit0",          "set_valve_bit0_sensor")
    await reg("valve_bit2",          "set_valve_bit2_sensor")
    await reg("valve_bit3",          "set_valve_bit3_sensor")
    await reg("valve_bit4",          "set_valve_bit4_sensor")
    await reg("valve_bit6",          "set_valve_bit6_sensor")
    # Pump bits
    await reg("pump_bit0",           "set_pump_bit0_sensor")
    await reg("pump_bit1",           "set_pump_bit1_sensor")
    await reg("pump_bit2",           "set_pump_bit2_sensor")
    await reg("pump_bit4",           "set_pump_bit4_sensor")
    await reg("pump_bit7",           "set_pump_bit7_sensor")
    # Counters
    await reg("hours_run_pump",               "set_hours_run_pump_sensor")
    await reg("hours_run_3way",               "set_hours_run_3way_sensor")
    await reg("hours_run_ch",                 "set_hours_run_ch_sensor")
    await reg("hours_run_dhw",                "set_hours_run_dhw_sensor")
    await reg("power_supply_aval_hours",      "set_power_supply_aval_hours_sensor")
    await reg("pump_starts",                  "set_pump_starts_sensor")
    await reg("number_of_3way_valve_cycles",  "set_number_of_3way_valve_cycles_sensor")
    await reg("burner_start_dhw",             "set_burner_start_dhw_sensor")
    await reg("total_burner_start",           "set_total_burner_start_sensor")
    await reg("failed_burner_start",          "set_failed_burner_start_sensor")
    await reg("number_flame_loss",            "set_number_flame_loss_sensor")
