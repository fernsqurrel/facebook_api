from dotenv import load_dotenv, find_dotenv
import os
import pandas as pd
import requests
from collections import defaultdict


def find_user_token():
    load_dotenv(find_dotenv())

    user_token = os.getenv("user_token")
    return user_token


def find_user_id():
    load_dotenv(find_dotenv())

    user_id = os.getenv("user_id")
    return user_id


def find_page_id():
    load_dotenv(find_dotenv())

    page_id = os.getenv("page_id")
    return page_id


def find_page_token(user_id=None, user_token=None):
    if user_id is None:
        user_id = find_user_id()
    if user_token is None:
        user_token = find_user_token()

    page_token_url = (
        f"https://graph.facebook.com/{user_id}/accounts?access_token={user_token}"
    )

    res = requests.get(page_token_url)
    res_json = res.json()

    try:
        page_token = res_json["data"][0]["access_token"]
    except KeyError:
        print("Error loading using user token - using saved page token")
        page_token = os.getenv("page_token")
    return page_token


def request_metrics(list_of_metrics, page_token=None):
    """
    Give me a list of metrics and a page token and I'll return the value (dated at the most recent time)
    Output can be given straight to pandas to pd.Dataframe.from_dict --> df.to_excel
    """

    if page_token is None:
        page_token = find_page_token()

    base_url = "https://graph.facebook.com"

    object_id = find_page_id()
    metric_string = ",".join(list_of_metrics)
    add_on_url = f"/v10.0/{object_id}/insights/{metric_string}"

    url = base_url + add_on_url

    params = {
        "access_token": page_token,
        "show_description_from_api_doc": "true",
        "period": "days_28",
    }

    res = requests.get(url, params=params)

    d = dict(res.json())

    return d


def data_to_dict(d):
    """This should take in the DATA from a request (this can be done with res.json()['data'])
    And it will output a defaultdict of defaultdicts with the structure
    date --> metric --> value
    """
    output_d = defaultdict(defaultdict)

    # This is how the output_d will be structured when it's returned
    # output_d['date']['metric'] = value

    # Iterating through each metric that we're given
    for ele in d:
        variable_name = ele["name"]

        # Iterating through each value for a specific metric
        for values in ele["values"]:
            # There should be a list of values, each for a different date
            # Structure of this is a list of dicts
            # We should turn metric -> date -> value into date -> metric -> value

            # We wrap this in a try because some metrics don't come as integers (they could be a list or a dict)
            try:
                if isinstance(values["value"], int) == True:
                    date = values["end_time"]
                    value = values["value"]
                    metric_name = variable_name

                    output_d[date][metric_name] = value
            except Exception:
                continue

    return output_d


# Parameter for index should be removed in df.to_excel
def dict_to_spreadsheet(d, filename="output.xlsx"):
    """This takes in a dict and outputs the spreadsheet to the given filename"""
    df = pd.DataFrame.from_dict(d)
    df.to_excel(filename)


def debug_token(token):

    payload = {"input_token": token}

    base_url = "https://graph.facebook.com"
    extension = f"/v10.0/debug_token?input_token={token}"

    url = base_url + extension

    res = requests.get(url, data=payload).json()

    return res


def find_published_posts(page_token=None, page_id=None):
    if page_token is None:
        page_token = find_page_token()

    if page_id is None:
        page_id = find_page_id()

    base_url = "https://graph.facebook.com"
    add_on_url = f"/v10.0/{page_id}/published_posts"
    url = base_url + add_on_url

    params = {"access_token": page_token}

    res = requests.get(url, params=params)

    d = res.json()

    post_ids = [ele["id"] for ele in d["data"]]

    return post_ids


if __name__ == "__main__":
    print("Hello World!")
