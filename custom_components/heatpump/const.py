"""Constants for the Heat Pump integration."""

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntityDescription
)

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import ENERGY_WATT_HOUR, POWER_WATT, Platform, PERCENTAGE

DOMAIN = "heatpump"

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR] #integration

COORDINATOR = "coordinator"
NAME = "name"

SENSORS = (
    SensorEntityDescription(
        key="daily_production",
        name="Today's Energy Production",
        native_unit_of_measurement=ENERGY_WATT_HOUR,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
    ),
)

BINARY_SENSORS = BinarySensorEntityDescription(
    key="grid_status",
    name="Grid Status",
    device_class=BinarySensorDeviceClass.CONNECTIVITY
)
