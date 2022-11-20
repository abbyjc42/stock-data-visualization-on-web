'''
This web service extends the Alphavantage api by creating a visualization module, 
converting json query results retuned from the api into charts and other graphics. 

This is where you should add your code to function query the api
'''
import requests
import pygal
from datetime import date, datetime
import json
import lxml

# Constant for the API key
API_KEY = "AH4E9KX41PXBFQQI"

#Helper function for converting date
def convert_date(str_date):
    return datetime.strptime(str_date, '%Y-%m-%d').date()

# Function for building a query URL using provided parameters from the form
def build_URL(time_selection, symbol):
    if time_selection[0] != "":
        global ogURL
        ogURL = "https://www.alphavantage.co/query?function={}&symbol={}&interval={}&apikey={}".format(time_selection[0], symbol, time_selection[1], API_KEY)
    else:
        ogURL = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(time_selection[0], symbol, API_KEY)

    test_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo"
    # return ogURL
    return test_URL

# Function that parses the JSON query results into useable data for the chart
def parse_json(request_url, date_range, time_series):
    response = requests.get(request_url).text
    response_data = json.loads(response)

    data_title = ""
    data = []
    if time_series[0] == "TIME_SERIES_INTRADAY":
        # Time Series (5min)
        data_title = "Time Series ({})".format(time_series[1])
    elif time_series[0] == "TIME_SERIES_DAILY":
        data_title = "Time Series (Daily)"
    elif time_series[0] == "TIME_SERIES_WEEKLY":
        data_title = "Weekly Time Series"
    elif time_series[0] == "TIME_SERIES_MONTHLY":
        data_title = "Monthly Time Series"

    date_format = ''
    if data_title == "Time Series ({})".format(time_series[1]):
        date_format = '%Y-%m-%d %H:%M:%S'
    else:
        date_format = '%Y-%m-%d'

    for entry in response_data[data_title]:
        raw_datetime = datetime.strptime(entry, date_format)
        if raw_datetime >= date_range[0] and raw_datetime <= date_range[1]:
            data.append({'Date':entry, 'Data':response_data[data_title][entry]})

    return data

# Function that generates coordinates from the JSON raw data to use for generating the chart
def generate_coordinates(raw_data, y_title):
    coordinates = [[], []]  # 0 index is all X values, 1 index is all Y values
    date_format = '%Y-%m-%d'
    try:
        test_coordinate = datetime.strptime(raw_data[0]['Date'], date_format)
    except ValueError:
        date_format = '%Y-%m-%d %H:%M:%S'

    for element in raw_data:
        coordinates[0].append(datetime.strptime(element['Date'], date_format))
        coordinates[1].append(float(element['Data'][y_title]))
        # Test print statement
        #print("X: {}\nY: {}".format(element['Date'], element['Data'][y_title]))
    return coordinates

def generate_graph(symbol, chart_type, open_line, high_line, low_line, close_line):
    chart = pygal.Bar()
    if chart_type == "Line":
        chart = pygal.Line()
    
    chart.title = 'Stock Data for {}: {} to {}'.format(symbol, open_line[0][0], open_line[0][-1])
    chart.x_labels = map(lambda d: d.strftime('%Y-%m-%d'), open_line[0])
    chart.add('Open', open_line[1])
    chart.add('High', high_line[1])
    chart.add('Low', low_line[1])
    chart.add('Close', close_line[1])

    return chart