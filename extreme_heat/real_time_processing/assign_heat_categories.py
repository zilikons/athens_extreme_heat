import pandas as pd
from extreme_heat.real_time_processing.nws_heat_index import heat_index

import pandas as pd

def check_heatwave_conditions(climate_data_df: pd.DataFrame) -> pd.DataFrame:
    df = climate_data_df.copy()
    # Calculate minimum and maximum heat index temperature, as well as mean wind speed for each day
    df['heat_index'] = df.apply(lambda x: heat_index(x['temperature'], x['humidity']), axis=1)
    days = df['day'].unique()
    classified_days = {}

    for day in days:
        condition_1, condition_2, condition_3 = False, False, False
        min_temp = df[df['day'] == day]['heat_index'].min()
        max_temp = df[df['day'] == day]['heat_index'].max()
        mean_wind_speed = df[df['day'] == day]['wind_speed'].mean()

        # Check if the conditions are met for a heatwave classification
        if min_temp >= 26:
            condition_1 = True
        if max_temp >= 39:
            condition_2 = True
        if mean_wind_speed <= 5.5:
            condition_3 = True

        if condition_1 and condition_2 and condition_3:
            classified_days[day] = 3
        elif (condition_1 or condition_2) and condition_3:
            classified_days[day] = 2
        elif condition_1 or condition_2:
            classified_days[day] = 1
        else:
            classified_days[day] = 0

    # Check if three consecutive days are heatwave days (class 3)
    consecutive_heatwaves = [k for k, v in classified_days.items() if v == 3]
    for i in range(len(consecutive_heatwaves) - 2):
        if consecutive_heatwaves[i] + 1 == consecutive_heatwaves[i + 1] and consecutive_heatwaves[i] + 2 == consecutive_heatwaves[i + 2]:
            classified_days[consecutive_heatwaves[i]] = 4
            classified_days[consecutive_heatwaves[i + 1]] = 4
            classified_days[consecutive_heatwaves[i + 2]] = 4

    return classified_days


# if __name__ == "__main__":
    # print(temperature_to_category(51, input_units="celsius"))
    # print(temperature_to_category(350, input_units="kelvin"))
    # print(temperature_to_category(108, input_units="fahrenheit"))
