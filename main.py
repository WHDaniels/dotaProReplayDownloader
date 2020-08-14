"""
Application that downloads 'pro-level' Dota 2 replays of the specified hero to the Dota 2 replays directory.
Copyright (C) 2020  William Daniels under GNU General Public License (see License.md)
"""
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QApplication
from selenium import webdriver
import requests
import atexit
import time
import json
import os

"""
def findMatchUrlFinish(recents):
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

# gets the robots.txt file of the site and copies it to the program directory

# robotsTxt = requests.get("http://www.dota2protracker.com/robots.txt", allow_redirects=True)
# open('robots.txt', 'wb').write(robotsTxt.content)

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

from PyQt5 import QtCore, QtGui, QtWidgets
from gui import Ui_MainWindow


def downloadReplay(replayLink):
    print("Getting file name")
    # get the file name through splitting the link and truncating
    if replayLink.find('/'):
        fileName = replayLink.rsplit('/', 1)[1]
        fileName = fileName[0:-4]

    # read the data.json file in the data folder to get the dota 2 replays path
    with open("data//data.json", 'r') as file:
        directoryJson = json.load(file)

    # grab the path
    replaysDirectory = directoryJson["replayDirectory"]

    # if the replay attempting to be downloaded already exists
    # inside of the dota 2 replays folder, skip it
    for file in os.listdir(replaysDirectory):
        if file[0:-4] in fileName:
            print("Replay already downloaded!\n\n")
            return None

    print("Downloading replay to disk")
    # else, download the replay to that directory
    open(replaysDirectory + "/" + fileName, 'wb')
    print("Download Complete! You've downloaded to:")
    print(replaysDirectory + "/" + fileName + "\n\n")


def getReplayFolderSnapshot():
    # read the data.json file in the data folder to get the dota 2 replays path
    with open("data//data.json", 'r') as file:
        directoryJson = json.load(file)

    # grab the path
    replaysDirectory = directoryJson["replayDirectory"]

    replaysList = []

    for file in os.listdir(replaysDirectory):
        if '.dem' in file:
            replaysList.append(file)

    return replaysList


def getReplay(matchUrl, browser):
    browser.get(matchUrl)

    print("Waiting for page to load...")
    # give some time for the page to load before attempting to grab the href
    time.sleep(2)

    print("Getting replay link\n")
    # Parse the html of the opendota site to get the link to the replay of the match
    elements = browser.find_elements_by_xpath('//a[@href]')

    for a in elements:
        link = a.get_attribute("href")
        if link == "" or link is None:
            continue
        if "valve" in link:
            downloadReplay(link)


def playerGameList(browser, selectedHero):
    print("Waiting for page to load...")
    time.sleep(1)

    d2ptLink = "http://www.dota2protracker.com/hero/" + selectedHero
    browser.get(d2ptLink)

    playerList = []

    playerElement = browser.find_elements_by_css_selector('td.padding-cell.sorting_1 > a:nth-child(1)')
    for a in playerElement:
        playerList.append(a.text)

    gameList = []

    gameElement = browser.find_elements_by_css_selector('a:nth-child(3)')
    for a in gameElement:
        gameLink = a.get_attribute("href")
        if gameLink == "" or gameLink is None:
            continue
        if "opendota" in gameLink:
            gameList.append(gameLink)

    return playerList, gameList


def browsePressed():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.Directory)
    if dialog.exec_():
        directory = str(dialog.selectedFiles())
        directory = directory[2:len(directory) - 2]
        replayDirectory = {"replayDirectory": directory}
        with open("data\\data.json", 'w') as file:
            json.dump(replayDirectory, file)


def showPopup(replaysList, playerList, gameList):
    popup = QMessageBox()
    popup.setWindowTitle("Replays Downloaded")

    originalGameList = len(gameList)

    for x in reversed(range(len(gameList))):
        matchID = gameList[x].rsplit('/', 1)[-1]
        # only show games that were downloaded (not skipped)
        for file in replaysList:
            if matchID in file:
                gameList.pop(x)
                playerList.pop(x)
                break

    setText = []

    for y in range(len(gameList)):
        setText.append(playerList[y] + ": " + gameList[y] + "\t")

    setText.insert(0, "You've downloaded " + str(len(gameList)) + " replay(s): \n")

    duplicates = originalGameList - len(gameList)

    if duplicates > 0:
        setText.insert(0, "Of the " + str(originalGameList) + " replay(s) specified and available for download, \n"
                       + str(duplicates) + " is/are downloaded already. \n\n")

    setTextString = "\n".join(setText)
    popup.setText(setTextString)
    popup.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    popup.open()

    x = popup.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # local modifications to gui
        for x in range(114):
            self.ui.heroSelectCombo.addItem("")

        for x in range(22):
            self.ui.amountSelectCombo.addItem("")

        self.ui.heroSelectCombo.setItemText(0, QCoreApplication.translate("MainWindow", "Select Hero"))

        heroList = ["Abbadon", "Alchemist", "Ancient Apparition", "Anti-Mage", "Arc Warden", "Axe", "Bane", "Batrider",
                    "Beastmaster", "Bloodseeker", "Bounty Hunter", "Bounty Hunter", "Brewmaster", "Broodmother",
                    "Centaur Warrunner", "Chaos Knight", "Chen", "Clinkz", "Clockwerk", "Crystal Maiden", "Dark Seer",
                    "Dark Willow", "Dazzle", "Death Prophet", "Disruptor", "Doom", "Dragon Knight", "Drow Ranger",
                    "Earth Spirit", "Earthshaker", "Elder Titan", "Ember Spirit", "Enchantress", "Enigma",
                    "Faceless Void", "Grimstroke", "Gyrocopter", "Huskar", "Invoker", "Io", "Jakiro", "Juggernaut",
                    "Keeper of the Light", "Kunkka", "Legion Commander", "Leshrac", "Lich", "Lifestealer", "Lina",
                    "Lion", "Lone Druid", "Luna", "Lycan", "Magnus", "Mars", "Medusa", "Meepo", "Mirana", "Monkey King",
                    "Morphling", "Naga Siren", "Nature\'s Prophet", "Necrophos", "Night Stalker", "Nyx Assassin",
                    "Ogre Magi", "Omniknight", "Oracle", "Outworld Devourer", "Pangolier", "Phantom Assassin",
                    "Phantom Lancer", "Phoenix", "Puck", "Pudge", "Pugna", "Queen of Pain", "Razor", "Riki", "Rubick",
                    "Sand King", "Shadow Demon", "Shadow Fiend", "Shadow Shaman", "Skywrath Mage", "Spirit Breaker",
                    "Storm Spirit", "Sven", "Techies", "Templar Assassin", "Terrorblade", "Tidehunter", "Timbersaw",
                    "Tinker", "Tiny", "Treant Protector", "Troll Warlord", "Tusk", "Underlord", "Undying", "Ursa",
                    "Vengeful Spirit", "Venomancer", "Viper", "Visage", "Void Spirit", "Warlock", "Weaver",
                    "Windranger", "Winter Wyvern", "Witch Doctor", "Wraith King", "Zues"]

        for x in range(len(heroList)):
            self.ui.heroSelectCombo.setItemText(x + 1, QCoreApplication.translate("MainWindow", heroList[x]))

        self.ui.amountSelectCombo.setItemText(0, QCoreApplication.translate("MainWindow", "Select Amount"))
        for x in range(1, 21):
            self.ui.amountSelectCombo.setItemText(x, QCoreApplication.translate("MainWindow", str(x)))
        self.ui.amountSelectCombo.setItemText(21, QCoreApplication.translate("MainWindow", "All"))

        self.ui.downloadButton.clicked.connect(self.downloadPressed)
        self.ui.browseButton.clicked.connect(browsePressed)

    def downloadPressed(self):
        replaysList = getReplayFolderSnapshot()
        selectedHero = self.ui.heroSelectCombo.currentText().replace(" ", "%20")
        amount = int(self.ui.amountSelectCombo.currentText())

        # preparing options for chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        browser = webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe", options=options)

        playerList, gameList = playerGameList(browser, selectedHero)
        playerList, gameList = playerList[:amount], gameList[:amount]

        self.ui.progressBar.show()
        MainWindow.getRecentGames(self, browser, gameList)
        self.ui.progressBar.setProperty("value", 100)

        showPopup(replaysList, playerList, gameList)

    def getRecentGames(self, browser, gameList):

        downloadProgress = 0
        gameAmount = len(gameList)

        for game in gameList:
            getReplay(game, browser)

            downloadProgress += int((1 / gameAmount) * 100)
            self.ui.progressBar.setProperty("value", downloadProgress)
            QApplication.processEvents()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
