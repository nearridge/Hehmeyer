
# coding: utf-8

# In[15]:


import pandas as pd
from influxdb import DataFrameClient


def main(host='localhost', port=8086):

    user = "admin"
    password = 'root'
    dbname = 'demo'
    protocol = 'line'

    client = DataFrameClient(host, port, user, password, dbname)

    print("Create pandas DataFrame")
    df = pd.DataFrame(data=list(range(30)),
                      index=pd.date_range(start='2014-11-16',
                                          periods=30, freq='H'), columns=['0'])

    print("Create database: " + dbname)
    client.create_database(dbname)

    print("Write DataFrame")
    client.write_points(df, 'demo', protocol=protocol)

    print("Write DataFrame with Tags")
    client.write_points(df, 'demo',
                        {'k1': 'v1', 'k2': 'v2'}, protocol=protocol)

    print("Read DataFrame")
    client.query("select * from demo")

    print("Delete database: " + dbname)
    client.drop_database(dbname)


main()

