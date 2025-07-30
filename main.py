import requests
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# === CONFIGURAÇÕES DO INFLUXDB ===
bucket = "test-01"
org = "BB"
token = "PVb7F594ixoE7xyWMjftXT6pmbOM-he29VawsfRuHunDC0zqjQQevZoi70tXMbF7FTxotbTJI6YLsR_OhS64xQ=="
url = "http://localhost:8086"

# === API Externa (Open-Meteo) ===
weather_url = 'https://api.open-meteo.com/v1/forecast'
params = {
    'latitude': 48.85,
    'longitude': 2.35,
    'hourly': 'temperature_2m'
}

# === Buscar dados da API ===
response = requests.get(weather_url, params=params)
data = response.json()

times = data['hourly']['time']
temperatures = data['hourly']['temperature_2m']

# === Enviar dados para o InfluxDB ===
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

for t, temp in zip(times, temperatures):
    point = (
        Point("weather")
        .tag("location", "paris")
        .field("temperature", float(temp))
        .time(t, WritePrecision.NS)
    )
    write_api.write(bucket=bucket, org=org, record=point)

print("Dados enviados para o InfluxDB com sucesso.")
