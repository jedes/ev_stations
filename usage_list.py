# curl -d '["3b492339-5d5e-4a81-9019-f82ed6e69a90","f6e31d4c-d96c-4602-848a-c605e8766ace","f7472a54-e3f9-444e-b7e4-9d8cb15a332f","04fee987-7d0c-44da-a36f-ea3f8f8d74d3","df1665c6-d163-49dc-849a-d6db13816881","f22dcc51-e426-48ae-a7c2-c6439798e2a3"]' -X POST -H "Content-Type: application/json; charset=utf-8"  https://account.flo.ca/api/network/stations

import pickle
from requests_futures.sessions import FuturesSession
#import mysql.connector

#db = mysql.connector.connect(
#  host="localhost",
#  user="papa",
#  passwd="yourpassword",
#  database = "circuit_elec")

session = FuturesSession()
futures=[]

with open('stations_list.dat', 'rb') as infile:
    while True:
        try:
            station = pickle.load(infile)
        except EOFError:
            break

        futures.append(session.post('https://account.flo.ca/api/network/stations',
             headers={'Content-Type': 'application/json; charset=utf-8',
                      'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'},
             json=station['Ids']) )

for f in futures:
    r = f.result()
    if r.status_code != 200:
        continue

    stationinfo = r.json()
    for port in stationinfo['ports']:
        #db.cursor().execute("INSERT INTO usage_log (id, time, inuse) " +
        #                    "VALUES (%s, %s, %s)",
        #                    )
        #db.commit()
        print(port + ": " + stationinfo['ports'][port]['State'])
