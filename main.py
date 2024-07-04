# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import sys

from pmdarima import auto_arima
from tabulate import tabulate
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
import pmdarima
import warnings

warnings.filterwarnings("ignore")

def load_data(path):
    return pd.read_csv(path)


PARAMS = ['HUM', 'PM1', 'PM10', 'PM2_5', 'PRES', 'TC']


def pearson_correlation_analysis(data):
    new_data = {}
    for param in PARAMS:
        data_by_param = data[data['PARAMETER'] == param]
        new_data[param] = (list(data_by_param["VALUE"]))
    # print(new_data)
    data_corr = pd.DataFrame(new_data)
    # print(data_corr)

    # matrice corelatie
    correlation_matrix = data_corr.corr(method='pearson')

    print(correlation_matrix)


def mean_by_hour(data, parameter):
    data_by_param = data[data['PARAMETER'] == parameter]

    # std, mean, percentiles
    numeric_stats = data_by_param["VALUE"].describe(percentiles=[0.25, 0.5, 0.75]).transpose()

    # print(tabulate(numeric_stats, headers='keys', tablefmt='psql'))
    print(numeric_stats)

    # Media pe ora
    mean_by_hour = data_by_param.groupby('DateHour')['VALUE'].mean().reset_index()
    print(tabulate(mean_by_hour.head(20), headers='keys', tablefmt='psql'))

    mean_by_hour.plot(kind='scatter',
            x='DateHour',
            y='VALUE',
            color='red')

    # set the title
    plt.title("Data for " + parameter)

    # show the plot
    plt.show()

    return 0


def histogram(data, parameter):
    data_by_param = data[data['PARAMETER'] == parameter]
    plt.hist(data_by_param["VALUE"], bins=15, edgecolor='black')
    plt.title("Histogram for " + parameter)
    plt.show()


def hum_PM10_plot(data):
    new_data = {}
    data_by_param = data[data['PARAMETER'] == "HUM"]
    new_data["HUM"] = (list(data_by_param["VALUE"]))
    mean_by_hour_hum = data_by_param.groupby('DateHour')['VALUE'].mean().reset_index()

    # print(mean_by_hour_hum)

    data_by_param = data[data['PARAMETER'] == "PM10"]
    new_data["PM10"] = (list(data_by_param["VALUE"]))
    mean_by_hour_pm10 = data_by_param.groupby('DateHour')['VALUE'].mean().reset_index()

    hum_pm10_data = {}
    hum_pm10_data = {"HUM": list(mean_by_hour_hum["VALUE"]), "PM10": list(mean_by_hour_pm10["VALUE"])}

    df_hour_h_p = pd.DataFrame(hum_pm10_data)

    # print(df_hour_h_p)
    # Total plot
    h_p = pd.DataFrame(new_data)
    h_p.plot(kind="scatter",
             x='HUM',
             y='PM10',
             color='green')
    plt.title("HUM vs PM10")

    plt.show()

    # plot pe ora
    df_hour_h_p.plot(kind="scatter",
                     x='HUM',
                     y='PM10',
                     color='green')
    plt.title("Hourly HUM vs PM10")

    plt.show()


def sarimax_forecasting(data, nr):
    data_by_param = data[data['PARAMETER'] == "HUM"]
    mean_by_hour_hum = data_by_param.groupby('DateHour')['VALUE'].mean().reset_index()


    # # Normalizarea datelor
    # mean_by_hour_hum['VALUE'] = (mean_by_hour_hum['VALUE'] - mean_by_hour_hum['VALUE'].mean()) / mean_by_hour_hum[
    #     'VALUE'].std()

    # print(mean_by_hour_hum)
    humidity = mean_by_hour_hum["VALUE"]
    # model = auto_arima(humidity, seasonal=True, m=12, trace=True, error_action='ignore', suppress_warnings=True,
    #                    max_p=3, max_d=1, max_q=3, max_P=2, max_D=1, max_Q=2)
    # SARIMAX
    model = SARIMAX(mean_by_hour_hum["VALUE"].head(nr), order=(1, 0, 0), seasonal_order=(1, 1, 1, 24))
    model_fit = model.fit()

    # Urm 24 ore
    forecast = model_fit.forecast(steps=24)

    # plt.plot(mean_by_hour_hum['x'], mean_by_hour_hum['VALUE'], label='Date originale', marker='o')
    # plt.plot(mean_by_hour_hum['x'], forecast['VALUE'], label='Date prezise', linestyle='--')
    forecast_df = forecast.to_frame(name="VALUE")
    forecast_df["DateHour"] = mean_by_hour_hum.iloc[nr:nr+24]['DateHour']
    forecast_df = forecast_df.reset_index(drop=True)
    # print(forecast_df)

    plt.figure(figsize=(10, 5))
    plt.plot(mean_by_hour_hum['DateHour'].head(nr+24), mean_by_hour_hum['VALUE'].head(nr+24), label='Historical Data')
    plt.plot(forecast_df['DateHour'], forecast_df['VALUE'], label='Forecast', color='red')
    plt.xlabel('DateHour')
    plt.ylabel('Humidity')
    plt.title('Humidity Forecast for the Next 24 Hours')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # SVR AI

    parametru = sys.argv[1]
    data = load_data(parametru)
    data['DATE'] = pd.to_datetime(data['DATE'], format='%m/%d/%Y %H:%M')
    data['DateHour'] = data['DATE'].dt.strftime('%Y-%m-%d %H')
    # print(tabulate(data, headers='keys', tablefmt='psql'))

    # Plotare valori
    for parameter in PARAMS:
        mean_by_hour(data, parameter)

    # Pearson
    pearson_correlation_analysis(data)
    # Hum vs PM10
    hum_PM10_plot(data)

    for parameter in PARAMS:
        histogram(data, parameter)

    sarimax_forecasting(data, 1020)
