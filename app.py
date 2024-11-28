import urllib3
import boto3

from chalicelib.utils.ssm import get_value_parameter

from chalice import Chalice


app = Chalice(app_name="collector")
http = urllib3.PoolManager()
client_s3 = boto3.client(
    "s3",
    aws_access_key_id=get_value_parameter("ACCESS_KEY"),
    aws_secret_access_key=get_value_parameter("SECRET_KEY"),
)


@app.schedule("rate(1 minute)")
def periodic_task(event):
    apiKey = get_value_parameter("exchange-rate-api-key")
    response = http.request(
        "GET", f"https://v6.exchangerate-api.com/v6/{apiKey}/latest/BRL"
    ).json()

    euro = f"{1/response['conversion_rates']['EUR']}"
    dol = f"{1/response['conversion_rates']['USD']}"
    content = f"{response['time_last_update_utc']}: {euro} euros, {dol} dolares"

    client_s3.write_file(content, "exchange_rate.txt")
