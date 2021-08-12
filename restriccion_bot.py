# -*- coding: utf-8 -*-


"""
@author: jose.ariasq@gmail.com
"""


# System imports
from datetime import datetime
from dateutil import tz

# Third party imports
import pandas as pd
import tweepy

# User imports

RES_FILE_URL = (
    "https://raw.githubusercontent.com/ariasjose/restriccioncr/main/restriccion.csv"
)
CR_TZ = tz.gettz("America/Costa_Rica")
WEEKDAYS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
WEEKDAYS_LR = [
    [1, 2],
    [3, 4],
    [5, 6],
    [7, 8],
    [9, 0],
]


# authentication
CONSUMER_KEY = ""
CONSUMER_SECRET = ""
RESTRICCIONCR = {
    "oauth_token": "",
    "oauth_token_secret": "",
    "user_id": "",
    "screen_name": "",
}
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(RESTRICCIONCR["oauth_token"], RESTRICCIONCR["oauth_token_secret"])

api = tweepy.API(auth)


def lambda_handler(event, context):
    dt = datetime.now(tz=CR_TZ)
    # timestamp = dt.strftime("%d-%m-%y %I:%M%p")
    time_now = dt.strftime("%I:%M%p")
    dow = dt.weekday()

    try:
        # Monday - Friday
        if dow < 5:
            restricted_lp = WEEKDAYS_LR[dow]
            msg = f"{time_now} - #restriccioncr Hoy {WEEKDAYS[dow]} no circulan placas terminadas en {restricted_lp[0]} y {restricted_lp[1]}"
        else:
            # data = pd.read_csv("restriccion.csv", encoding="utf8")
            data = pd.read_csv(RES_FILE_URL, encoding="utf8")
            restricted_lp_weekends = dict(zip(data.md, data.r))
            key = f"{dt.month}-{dt.day}"
            msg = f"#restriccioncr Hoy no circulan placas {restricted_lp_weekends[key]}"

        api.update_status(status=msg)

        return {"statusCode": 200, "body": {"message": "Tweet successfully published!"}}

    except Exception as ex:
        return {
            "statusCode": 500,
            "body": {"message": "error publishing tweet!", "exception": str(ex)},
        }
