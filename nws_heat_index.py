import numpy as np

def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) * 5 / 9

def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32

def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

def celsius_to_kelvin(celsius):
    return celsius + 273.15

def heat_index(input_temperature, relative_humidity, input_units="celsius"):
    if input_units == "celsius":
        temperature_fahrenheit = celsius_to_fahrenheit(input_temperature)
    if input_units == "kelvin":
        temperature_fahrenheit = celsius_to_fahrenheit(kelvin_to_celsius(input_temperature))
    if input_units == "fahrenheit":
        temperature_fahrenheit = input_temperature
    if input_units not in ["celsius", "kelvin", "fahrenheit"]:
        raise ValueError("Invalid input_units, must be 'celsius', 'kelvin', or 'fahrenheit'")

    if temperature_fahrenheit < 40:
        print("Temperature is below 40F, returning input temperature")
        return input_temperature
    A_index = -10.3 + 1.1 * temperature_fahrenheit + 0.047 * relative_humidity
    if A_index < 79:
        print("A Index is below 79, returning input temperature")
        return fahrenheit_to_celsius(A_index)
    heat_index_fahrenheit = (
        -42.379
        + 2.04901523 * temperature_fahrenheit
        + 10.14333127 * relative_humidity
        - 0.22475541 * temperature_fahrenheit * relative_humidity
        - 6.83783e-3 * temperature_fahrenheit ** 2
        - 5.481717e-2 * relative_humidity ** 2
        + 1.22874e-3 * temperature_fahrenheit ** 2 * relative_humidity
        + 8.5282e-4 * temperature_fahrenheit * relative_humidity ** 2
        - 1.99e-6 * temperature_fahrenheit ** 2 * relative_humidity ** 2
    )

    if relative_humidity < 13 and 80 <= temperature_fahrenheit <= 112:
        adjustment = ((13 - relative_humidity) / 4) * np.sqrt((17 - abs(temperature_fahrenheit - 95)) / 17)
        heat_index_fahrenheit -= adjustment
        print(f"Adjustment: {adjustment:.2f}, condition 1")
    elif relative_humidity > 85 and 80 <= temperature_fahrenheit <= 87:
        adjustment = ((relative_humidity - 85) / 10) * ((87 - temperature_fahrenheit) / 5)
        heat_index_fahrenheit += adjustment
        print(f"Adjustment: {adjustment:.2f}, condition 2")
    print("No adjustment, returning heat index, condition 3")
    if input_units == "celsius":
        heat_index_result = fahrenheit_to_celsius(heat_index_fahrenheit)
    if input_units == "kelvin":
        heat_index_result = celsius_to_kelvin(fahrenheit_to_celsius(heat_index_fahrenheit))
    if input_units == "fahrenheit":
        heat_index_result = heat_index_fahrenheit
    return heat_index_result

# Example usage
if __name__ == "__main__":
    temperature_celsius = 30
    relative_humidity = 50
    heat_index_value = heat_index(temperature_celsius, relative_humidity, input_units="celsius")
    print(f"Heat Index (Celsius): {heat_index_value:.2f}")
