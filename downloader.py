import os
import requests
import json
import time

def download(startyear, endyear, foldername = None):
    """
    Downloads the court decisions for the given years through the Open Legal Data API and saves them in json files.

    :param int startyear: Earliest year from which decisions should be downloaded (will start from the first of January)
    :param int endyear: Last year from which decisions should be downloaded (will end on 31st of December)
    :param foldername: Folder under which the data should be stored (default folder will be startyear-endyear)
    :type priority: string or None
    """

    page = 23

    if(foldername is None):
        foldername = str(startyear) + "-" + str(endyear)

    if not os.path.exists(foldername):
        os.mkdir(foldername)

    url = "https://de.openlegaldata.io/api/cases/?court=&court__state=&court__jurisdiction=&court__slug=&o=-date&court__level_of_appeal=&format=json&"
    url += "date_after=" + str(startyear) + "-01-01&"
    url += "date_before=" + str(endyear) + "-12-31&"
    url += "page=" + str(page)

    r = requests.get(url)
    file = open(foldername + "/" + str(page) + ".json", 'w', encoding="utf-8")
    file.write(r.text)
    file.close()
    data = json.loads(r.text)

    # continue as long as more decisions are available
    while "next" in data and not data["next"] is None and len(data["next"]) > 3:
        page += 1
        r = requests.get(data["next"])
        file = open(foldername + "/" + str(page) + ".json", 'w', encoding="utf-8")
        file.write(r.text)
        file.close()
        data = json.loads(r.text)
        # make sure not to get blocked
        time.sleep(3)