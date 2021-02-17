
# coding: utf-8

# In[6]:


import pandas as pd
from influxdb import DataFrameClient
from datetime import datetime
from datetime import timedelta

def get_all_data(symbol, start_date, end_date):
    
    current_date = pd.Timestamp.now().date()
    if start_date > current_date or end_date > current_date or start_date > end_date:
        print("Invalid date entries")
        return

    temp_date = pd.Timestamp("1900-1-1").date()
    data = pd.DataFrame()
    c = 0

    while temp_date <= end_date:

        url = "https://www.bitmex.com/api/v1/funding?_format=csv&count=500&start="+str(c)+"&symbol=" + symbol + "&reverse=false"
        df_temp = pd.read_csv(url, parse_dates=['timestamp'])
        data = data.append(df_temp)
        c += 500
        temp_date = df_temp.loc[len(df_temp)-1, 'timestamp'].date()

    data['time'] = pd.to_datetime(data['timestamp'])
    data.insert(0, 'date', data['time'].dt.date)
    data.insert(1, 'funding_time', data['time'].dt.time)
    data = data.drop('time', axis=1)
    data = data[data['date'] >= start_date]
    data = data[data['date'] <= end_date]

    return data

def get_df():

    # maximum API query count is 500
    symbol = 'XBT'
    start_date = "2019-5-18" # year-month-date
    end_date = 'now' # year-month-date or "now"
    # start_date and end_date are inclusive

    start_date = pd.Timestamp(start_date).date()
    if end_date != 'now':
        end_date = pd.Timestamp(end_date).date()
    else:
        yesterday = datetime.today().date() - timedelta(days = 1)
        end_date = yesterday
        
    output = get_all_data(symbol, start_date, end_date)
    output = output.set_index('timestamp')
    return output

def main(host='localhost', port=8086):

    user = "admin"
    password = 'root'
    dbname = 'funding_rate'
    protocol = 'line'

    client = DataFrameClient(host, port, user, password, dbname)

    print("Create pandas DataFrame")
    df = get_df()

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Write DataFrame")
    client.write_points(df, 'funding_rate', protocol=protocol)

#     print("Write DataFrame with Tags")
#     client.write_points(df, 'demo',
#                         {'k1': 'v1', 'k2': 'v2'}, protocol=protocol)

#     print("Read DataFrame")
#     client.query("select * from demo")

#     print("Delete database: " + dbname)
#     client.drop_database(dbname)
    
main()

