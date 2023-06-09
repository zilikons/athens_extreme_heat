import pandas as pd
from extreme_heat.real_time_processing.assign_heat_categories import check_heatwave_conditions

def test_check_heatwave_conditions():
    data = {'temperature': [32, 33, 30, 36, 34, 38, 28, 29, 27, 20, 35, 37, 34],
            'humidity': [60, 50, 70, 65, 55, 75, 80, 85, 90, 35, 70, 72, 71],
            'wind_speed': [4, 6, 5, 3, 5, 4, 6, 7, 5, 4, 4, 5, 4],
            'day': [1, 1, 2, 2, 3, 3, 4, 4, 5, 6, 7, 8, 9]}

    df = pd.DataFrame(data)

    classified_days = check_heatwave_conditions(df)

    assert classified_days[1] == 2, f"Expected day 1 to be classified as 2, but got {classified_days[1]}"
    assert classified_days[2] == 3, f"Expected day 2 to be classified as 3, but got {classified_days[2]}"
    assert classified_days[3] == 3, f"Expected day 3 to be classified as 3, but got {classified_days[3]}"
    assert classified_days[4] == 1, f"Expected day 4 to be classified as 1, but got {classified_days[4]}"
    assert classified_days[5] == 2, f"Expected day 5 to be classified as 2, but got {classified_days[5]}"
    assert classified_days[6] == 0, f"Expected day 6 to be classified as 0, but got {classified_days[6]}"
    assert classified_days[7] == 4, f"Expected day 7 to be classified as 4, but got {classified_days[7]}"
    assert classified_days[8] == 4, f"Expected day 8 to be classified as 4, but got {classified_days[8]}"
    assert classified_days[9] == 4, f"Expected day 9 to be classified as 4, but got {classified_days[9]}"

    print("All tests passed.")

test_check_heatwave_conditions()
