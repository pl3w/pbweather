from asyncio.log import logger
import requests
import pandas as pd
from router import Router


def get_data():
    print("Get Task!")
    # Request data
    response = requests.get("https://data.epa.gov.tw/api/v2/aqx_p_432?format=json&api_key=2cb603b2-1507-46c8-85c0-93e5107d773d")

    # Check error.
    try:
        response.json()
    except:
        return

    df = pd.DataFrame(response.json()['records']).set_index("sitename")
    df = clear_data(df)

    store_data(df)


def clear_data(df):
    df = df.drop('county', axis=1)
    df = df.drop('longitude', axis=1)
    df = df.drop('latitude', axis=1)
    df = df.drop('siteid', axis=1)
    df.rename(columns = {"pm2.5": "pm25", "pm2.5_avg": "pm25_avg"}, inplace=True)
    df.replace('-', 0, inplace=True)
    df.replace('', 0, inplace=True)
    return df


def store_data(df):

    db_router = Router()

    try:
        df.to_sql(
            name = 'sitedata', 
            con = db_router.mysql_aqidb_conn(), 
            if_exists="append",
        )

    except Exception as e:
        logger.info(e)


if __name__ == "__main__":
    get_data()