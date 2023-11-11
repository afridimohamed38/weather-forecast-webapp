import requests
from datetime import datetime
import os

API_KEY = os.getenv("API_KEY")
ini = 0
time_list = [0]
for val in range(0, 7):
    ini += 3
    time_list.append(ini)


def get_raw_dates(filtered_data):
    """
    Get raw dates for the requested days used as a subfunction
    :rtype: object
    """
    date_list = []
    for index, val_2 in enumerate(filtered_data):
        dt = val_2['date']
        date_list.append(dt)
    return date_list


def get_temperatures(filtered_data):
    """
    Get temperature values for requested date and hour used a sub function
    """
    temperature_list = []
    for val_3 in filtered_data:
        t = val_3['day']['avgtemp_c']
        temperature_list.append(float(t))
    return temperature_list


def get_dates_data(place, days=1):
    """
    Getting date information from api
    :param place:
    :param days:
    """
    for val_1 in time_list:
        url = f"https://api.weatherapi.com/v1/forecast.json?q={place}&days={days}&hour={val_1}&key={API_KEY}"
        api_result = requests.get(url)
        api_response = api_result.json()
        filtered_data = api_response['forecast']['forecastday']  # this is a list
        # print(filtered_data)
        raw_date_list = get_raw_dates(filtered_data)

    return raw_date_list


def get_image_paths(filtered_data):
    """
    Get the image location from api repsonse and supply as input for sky data
    :param filtered_data:
    :return:
    """
    img_list = []
    for image_name in filtered_data:
        url_path = image_name['day']['condition']['icon']
        image_path = url_path.replace("//cdn.weatherapi.com", "images")
        img_list.append(image_path)
    return img_list


def get_dates_temperatures_data(place, srtd_dates_list):
    """
    Gets the final date and temperature date in correct order
    :param place:
    :param srtd_dates_list:
    :return:
    """
    dt_list = []
    temp_list = []
    image_path_list = []

    for dt in srtd_dates_list:
        for index, val_1 in enumerate(time_list):
            url = f"https://api.weatherapi.com/v1/forecast.json?q={place}&dt={dt}&hour={val_1}&key={API_KEY}"
            api_result = requests.get(url)
            api_response = api_result.json()
            filtered_data = api_response['forecast']['forecastday']  # this is a list
            # print(filtered_data)
            dt_val = get_raw_dates(filtered_data)[0]
            dt_list.append(dt_val)

            tp_val = get_temperatures(filtered_data)[0]
            temp_list.append(tp_val)

            image_path = get_image_paths(filtered_data)[0]
            image_path_list.append(image_path)
    return dt_list, temp_list, image_path_list


def add_timestamp(sorted_dates_list):
    """
    Convert the final dates to timestamp for better plotting
    :param sorted_dates_list:
    :return:
    """
    time_series = [0, 3, 6, 9, 12, 15, 18, 21]
    mod_dts = []

    for unique_date in sorted_dates_list:
        dt_split = unique_date.split("-")
        for index, hr_timestamp in enumerate(time_series):
            yy = int(dt_split[0])
            mm = int(dt_split[1])
            dd = int(dt_split[2])
            hh = int(hr_timestamp)
            timestamp = datetime(yy, mm, dd, hh)
            timestamp = timestamp.isoformat()
            timestamp = timestamp.replace("T", " ")
            value = f"{timestamp}"
            mod_dts.append(value)

    return mod_dts


if __name__ == "__main__":
    raw_dates = get_dates_data(place="Tokyo", days=2)
    print(raw_dates)
    print("*****************************************")
    print("set", sorted(set(raw_dates)))

    sorted_dates = sorted(set(raw_dates))

    f_dates, f_temperatures, image_paths = get_dates_temperatures_data(place="Tokyo", srtd_dates_list=sorted_dates)
    print("*****************************************")
    print(f_dates)
    print(f_temperatures)
    print(time_list)

    print("Hi")
    dates_timestamp = add_timestamp(sorted_dates)
    print(dates_timestamp)
    print(image_paths)
