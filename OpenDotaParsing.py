from selenium import webdriver
import requests
import atexit
import time
import json
import os


def findMatchUrlAndExecuteRest(recents):
    print("Creating json")
    # writes a json file containing the players recent match data
    with open(id + '.json', 'w') as file:
        json.dump(recents.json(), file, sort_keys=True, indent='\t')

    print("Reading recent matches from json")
    # opens the json for reading
    with open(id + '.json', 'r') as file:
        recentMatches = json.load(file)

    print("Finding specific hero matches\n")
    # looks at every match and records the match url of the game they play the specified hero
    # (since recentMatches is an array of json objects, it can be interpreted into python as a
    # list of dictionaries so iterate through each object to find where the hero_id = specified hero
    for match in recentMatches:
        if match["hero_id"] == 1:
            heroMatch = match["match_id"]
            heroMatchUrl = "https://www.opendota.com/matches/" + str(heroMatch)
            getReplay(heroMatchUrl)


def getReplay(matchUrl):
    # the location of executable 'chromedriver' in the program directory is essential for operation
    print("Preparing the option for the chrome driver")
    # prepare the option for the chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    print("Starting chrome browser")
    # start the chrome browser
    browser = webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe", options=options)
    browser.get(matchUrl)

    print("Waiting for page to load...")
    # give some time for the page to load before attempting to grab the href
    time.sleep(1)

    print("Getting replay link\n")
    # Parse the html of the opendota site to get the link to the replay of the match
    elements = browser.find_elements_by_xpath('//a[@href]')
    for a in elements:
        link = a.get_attribute("href")
        if link == "" or link is None:
            continue
        if "valve" in link:
            downloadReplay(link)


def downloadReplay(replayLink):
    print("Getting file name")
    # get the file name through splitting the link and truncating
    if replayLink.find('/'):
        fileName = replayLink.rsplit('/', 1)[1]
    fileName = fileName[0:-4]

    print("Downloading replay to disk")
    # specify the path to the dota 2 replays folder
    completePath = "C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/replays/"
    if not os.path.exists(completePath):
        completePath = "E" + completePath[1:]
        if not os.path.exists(completePath):
            print("Replay directory not found. Your Dota 2 replays folder is either missing or "
                  "is installed on a drive with a letter assignment that is neither 'C:' nor 'E:'")

    # Download the replay to that directory
    open(completePath + fileName, 'wb').write(parseRecents.content)
    print("Download Complete! You've downloaded to:")
    print(completePath + fileName + "\n\n")


# deletes the json (located in this programs directory) that contains the players recent games
def deleteJsonOnFinish(id):
    jsonPath = os.getcwd() + "\\" + id + ".json"
    print("Deleting: " + jsonPath)
    try:
        os.remove(jsonPath)
    except OSError as e:
        print("Error: %s : %s" % (jsonPath, e.strerror))


# deletes all json files in the program directory
def deleteAllJsons():
    filesInDirectory = os.listdir(os.getcwd())
    jsonFiles = [file for file in filesInDirectory if file.endswith(".json")]
    for file in jsonFiles:
        jsonPath = os.getcwd() + "\\" + file;
        print("Deleting: " + jsonPath)
        os.remove(jsonPath)


# executes deleteAllJsons() when program is exited
atexit.register(deleteAllJsons)

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

# main loop
for id in playerId:
    print("\n--------------------------------------")
    parseRecents = requests.get("https://api.opendota.com/api/players/" + id + "/recentMatches", allow_redirects=True)

    findMatchUrlAndExecuteRest(parseRecents)

    deleteJsonOnFinish(id)

"""
To be added: 1) UI
             2) automatic hero detection (find sufficiently high mmr players that play a certain hero
                alot without manually finding them and parse those players' recent matches)
"""
