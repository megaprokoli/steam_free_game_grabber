import requests
import json

import constants as const


def get_wishlist(user_id):
    resp = requests.get(const.WISHLIST_EP.format(user_id))
    ids = list(json.loads(resp.content).keys())
    return [const.STEAM_APP_URL + i for i in ids]


def appid_to_name(appid):
    resp = requests.get(const.APPDETAIL_EP,
                        params={"appids": appid})  # only 1 appid bc server returns null on multiple (see doc)

    if resp.status_code == 200:
        json_obj = json.loads(resp.content)
        return json_obj[appid]["data"]["name"]
