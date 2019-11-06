# InfluxDB

## Downloads 
Datasets from:
- Shootings: https://www.gunviolencearchive.org
- Tweets: http://www.trumptwitterarchive.com/archive

## Datasets 
- Tweets: /Tweets/20191031_TrumpTweets.txt
- Shootings: /Shootings/MassShooting.txt

## Converter 
- csv2lineShootings.py
- csv2lineShootings.py

## Setup 
Install InfluxDB and Chronograf or Grafana

### InfluxDB
1. Download Influx </br>
https://dl.influxdata.com/influxdb/releases/influxdb-1.7.9_darwin_amd64.tar.gz </br>
tar zxvf influxdb-1.7.9_darwin_amd64.tar.gz </br>
If not MacOS choose from here: https://portal.influxdata.com/downloads/</br>
2. Follow Instructions </br>
https://docs.influxdata.com/influxdb/v1.7/introduction/installation/

### Chronograf 
1. Download Chronograf </br>
https://dl.influxdata.com/chronograf/releases/chronograf-1.7.14_darwin_amd64.tar.gz
tar zxvf chronograf-1.7.14_darwin_amd64.tar.gz </br>
If not MacOS choose from here: https://portal.influxdata.com/downloads/</br>
2. Follow Instructions </br>
https://docs.influxdata.com/chronograf/v1.7/introduction/installation/ <br>

## Installing Data
Navigate to the path where Influx is in and start following command: </br>
`influx -import -path=<path> -precision=ms`

## Chronograf
 - Start Chronograf 
 - Define a Datasource 
   - InfluxDB as Source 
   - Trumpv2 as Database
 - Create a Dashboard 
 
Have fun!
