import time

import requests
import json
from urllib.parse import urlparse, urljoin
from selenium import webdriver
import os

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# These are some sample pro players whose games will be parsed for now
# Gabbi: https://www.opendota.com/players/152545459
# Timado: https://www.opendota.com/players/97658618
# Arteezy: https://www.opendota.com/players/86745912
# Miracle: https://www.opendota.com/players/105248644
# Crystallize: https://www.opendota.com/players/114619230
# Cooman: https://www.opendota.com/players/175463659
# Madara: https://www.opendota.com/players/95430068
# Raven: https://www.opendota.com/players/132309493
# 23savage: https://www.opendota.com/players/375507918
# Mason: https://www.opendota.com/players/315657960
# iLTW: https://www.opendota.com/players/113995822


playerId = ["152545459", "97658618", "86745912", "105248644", "114619230",
            "175463659", "95430068", "132309493", "375507918", "315657960", "113995822"]

# Parse all of their recent games to see if {hero_you_want_to_practice} matches
# the hero_id in their recent games (with "https://api.opendota.com/api/players/{account_id}/recentMatches")

# And then get the {match_id} of the most recent games where hero id is {hero_you_want_to_practice}

for id in playerId:
    parseRecents = requests.get("https://api.opendota.com/api/players/" + id + "/recentMatches", allow_redirects=True)
    with open(id + '.json', 'w') as file:
        json.dump(parseRecents.json(), file, sort_keys=True, indent='\t')

    with open(id + '.json', 'r') as file:
        recentMatches = json.load(file)
        for match in recentMatches:
            if match["hero_id"] == 1:
                heroMatch = match["match_id"]
                matchUrl = "https://www.opendota.com/matches/" + str(heroMatch)

                # the location of executable 'chromedriver' (C:\Users\mercm\PycharmProjects\OpenDotaStuff\chromedriver.exe)
                # is added to path environment variable, removal or movement of this executable without updating the path
                # will result in program errors

                # prepare the option for the chrome driver
                options = webdriver.ChromeOptions()
                options.add_argument('headless')

                # start chrome browser
                browser = webdriver.Chrome(options=options)
                browser.get(matchUrl)

                #delay = 5
                #try:
                #    myElem = WebDriverWait(browser, delay).until(
                #        EC.presence_of_all_elements_located((By.XPATH, '//a[@href]')))
                #    print("Loading complete!")
                #except TimeoutException:
                #    print("Loading took too much time!")

                time.sleep(7)

                # Parse the html of the opendota site to get the link to the replay of that match
                elements = browser.find_elements_by_xpath('//a[@href]')

                for a in elements:
                    href = a.get_attribute("href")
                    if href == "" or href is None:
                        continue
                    if "valve" in href:
                        break

                # Download the replay to the dota2 replays directory
                if href.find('/'):
                    fileName = href.rsplit('/', 1)[1]
                fileName = fileName[0:-4]

                completePath = "C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/replays/"
                if not os.path.exists(completePath):
                    completePath = "E" + completePath[1:]
                    if not os.path.exists(completePath):
                        print("Replay directory not found. Your Dota 2 replays folder is either missing or "
                              "is installed on a drive with a letter assignment of neither 'C:' nor 'E:'")
                print(completePath + fileName)
                print(matchUrl)
                open(completePath + fileName, 'wb').write(parseRecents.content)

# what can be added: 1) UI
#                    2) automatic hero detection (find sufficiently high mmr players that
#                       play a certain hero alot without manually finding them and parse those players)


# need to fix:  1) substitute for 'time.sleep'
#               2) delete jsons after they are made in project directory
#               3) refactor into functions and clean up code