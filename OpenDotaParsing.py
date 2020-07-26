from selenium import webdriver
import requests
import atexit
import time
import json
import os

"""
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
            heroMatch = str(match["match_id"])
            heroMatchUrl = "https://www.opendota.com/matches/" + heroMatch
            getReplay(heroMatchUrl)
"""

def getRecentGames(selectedHero, amount):
    d2ptLink = "http://www.dota2protracker.com/hero/" + selectedHero

    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    browser = webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe", options=options)
    browser.get(d2ptLink)

    print("Waiting for page to load...")
    time.sleep(1)

    playerNameList = []
    playerNameElement = browser.find_elements_by_css_selector('td.padding-cell.sorting_1 > a:nth-child(1)')
    for a in playerNameElement:
        playerNameList.append(a.text)

    gameList = []
    gameElement = browser.find_elements_by_css_selector('a:nth-child(3)')
    for a in gameElement:
        gameLink = a.get_attribute("href")
        if gameLink == "" or gameLink is None:
            continue
        if "opendota" in gameLink:
            gameList.append(gameLink)

    print("\n")
    for x in range(len(gameList[:amount])):
        print(playerNameList[x] + ": " + gameList[x])
    print("\n")

    for game in gameList[:amount]:
        getReplay(game)

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
    # open a requests to the replay link
    # replay = requests.get(replayLink, allow_redirects=True)

    # specify the path to the dota 2 replays folder
    completePath = "C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/replays/"
    if not os.path.exists(completePath):
        completePath = "E" + completePath[1:]
        if not os.path.exists(completePath):
            print("Replay directory not found. Your Dota 2 replays folder is either missing or "
                  "is installed on a drive with a letter assignment that is neither 'C:' nor 'E:'")

    # Download the replay to that directory
    open(completePath + fileName, 'wb')
    print("Download Complete! You've downloaded to:")
    print(completePath + fileName + "\n\n")

"""
# deletes the json (located in this programs directory) that contains the current player's recent games
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
"""

# main
print("What is the hero you want to download replays of?")
selectedHero = input()
print("How many of the most recent replays do you want to download?")
amount = int(input())

getRecentGames(selectedHero, amount)








# To be added: 1) UI

