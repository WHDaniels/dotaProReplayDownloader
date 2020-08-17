"""
Application that downloads 'pro-level' Dota 2 replays of the specified hero to the Dota 2 replays directory.
Copyright (C) 2020  William Daniels under GNU General Public License (see License.md)
"""

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QMainWindow, QApplication
from selenium import webdriver
import time
import json
import os

# gets the robots.txt file of the site and copies it to the program directory
# robotsTxt = requests.get("http://www.dota2protracker.com/robots.txt", allow_redirects=True)
# open('robots.txt', 'wb').write(robotsTxt.content)

from PyQt5 import QtCore, QtWidgets
from gui import Ui_MainWindow


def getReplaysDirectory():
    # read the data.json file in the data folder to get the dota 2 replays path
    with open("data//data.json", 'r') as file:
        directoryJson = json.load(file)

    # return the path
    return directoryJson["replayDirectory"]


def downloadReplay(replayLink):
    print("Getting file name")
    # get the file name through splitting the link and truncating
    fileName = replayLink.rsplit('/', 1)[1][0:-4]

    print("Downloading replay to disk")
    # download the replay to the replays directory
    open(getReplaysDirectory() + "/" + fileName, 'wb')
    print("Downloaded to: " + getReplaysDirectory() + "/" + fileName)


# gets a snapshot of the replay directory before downloading replays
def getReplayFolderSnapshot():
    replaysList = []

    # add every replay file in the replays directory to 'replaysList'
    for file in os.listdir(getReplaysDirectory()):
        if '.dem' in file:
            replaysList.append(file)

    return replaysList


def getReplay(matchUrl, browser):
    # get the opendota page of the match specified by 'matchUrl'
    browser.get(matchUrl)

    print("Waiting for page to load...")
    # give some time for the page to load before attempting to grab the href
    time.sleep(2)

    print("Getting replay link\n")
    # Parse the html of the opendota site to get the link to the replay of the match
    elements = browser.find_elements_by_xpath('//a[@href]')

    # parse every href tag
    for a in elements:
        link = a.get_attribute("href")
        if link == "" or link is None:
            continue
        # and if it is the link to the replay, download it
        if "valve" in link:
            downloadReplay(link)


def playerGameList(browser, selectedHero):
    print("Waiting for page to load...")
    time.sleep(1)

    # get the link to the page of the hero specified
    d2ptLink = "http://www.dota2protracker.com/hero/" + selectedHero
    browser.get(d2ptLink)

    playerList = []

    # keep track of every player playing the hero
    playerElement = browser.find_elements_by_css_selector('td.padding-cell.sorting_1 > a:nth-child(1)')
    for a in playerElement:
        playerList.append(a.text)

    gameList = []

    # keep track of every opendota link to every match
    gameElement = browser.find_elements_by_css_selector('a:nth-child(3)')
    for a in gameElement:
        gameLink = a.get_attribute("href")
        if gameLink == "" or gameLink is None:
            continue
        if "opendota" in gameLink:
            gameList.append(gameLink)

    return playerList, gameList


# allows the user to select the replays directory they would like to install to
def browsePressed():
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.Directory)

    if dialog.exec_():
        directory = str(dialog.selectedFiles())
        directory = directory[2:len(directory) - 2]
        replayDirectory = {"replayDirectory": directory}
        with open("data\\data.json", 'w') as file:
            json.dump(replayDirectory, file)


# after downloading, displays a popup showing the matches that have been downloaded,
# and how many duplicate matches (matches attempting to be downloaded that have already
# been downloaded) were detected and skipped
def showPopup(replaysList, playerList, gameList):
    popup = QMessageBox()
    popup.setWindowTitle("Replays Downloaded")

    # the original list of games before removing duplicates
    originalGameList = len(gameList)

    for x in reversed(range(len(gameList))):
        matchID = gameList[x].rsplit('/', 1)[-1]
        # only show games that were downloaded (not skipped) in these lists
        for file in replaysList:
            if matchID in file:
                gameList.pop(x)
                playerList.pop(x)
                break

    setText = []

    for y in range(len(gameList)):
        setText.append(playerList[y] + ": " + gameList[y] + "\t")

    setText.insert(0, "You've downloaded " + str(len(gameList)) + " replay(s): \n")

    # the amount of duplicate games is the amount original games minus the list without duplicates
    duplicates = originalGameList - len(gameList)

    if duplicates > 0:
        setText.insert(0, "Of the " + str(originalGameList) + " replay(s) specified and available for download, \n"
                       + str(duplicates) + " is/are downloaded already. \n\n")

    if len(gameList) == 0:
        setText.insert(2, ":(")

    setTextString = "\n".join(setText)
    popup.setText(setTextString)
    popup.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

    popup.open()

    x = popup.exec_()


# gui for the program
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # start local modifications to gui
        for x in range(114):
            self.ui.heroSelectCombo.addItem("")

        for x in range(22):
            self.ui.amountSelectCombo.addItem("")

        self.ui.heroSelectCombo.setItemText(0, QCoreApplication.translate("MainWindow", "Select Hero"))

        heroList = ["Abbadon", "Alchemist", "Ancient Apparition", "Anti-Mage", "Arc Warden", "Axe", "Bane", "Batrider",
                    "Beastmaster", "Bloodseeker", "Bounty Hunter", "Brewmaster", "Broodmother", "Centaur Warrunner",
                    "Chaos Knight", "Chen", "Clinkz", "Clockwerk", "Crystal Maiden", "Dark Seer", "Dark Willow",
                    "Dazzle", "Death Prophet", "Disruptor", "Doom", "Dragon Knight", "Drow Ranger", "Earth Spirit",
                    "Earthshaker", "Elder Titan", "Ember Spirit", "Enchantress", "Enigma", "Faceless Void",
                    "Grimstroke", "Gyrocopter", "Huskar", "Invoker", "Io", "Jakiro", "Juggernaut",
                    "Keeper of the Light", "Kunkka", "Legion Commander", "Leshrac", "Lich", "Lifestealer", "Lina",
                    "Lion", "Lone Druid", "Luna", "Lycan", "Magnus", "Mars", "Medusa", "Meepo", "Mirana", "Monkey King",
                    "Morphling", "Naga Siren", "Nature\'s Prophet", "Necrophos", "Night Stalker", "Nyx Assassin",
                    "Ogre Magi", "Omniknight", "Oracle", "Outworld Devourer", "Pangolier", "Phantom Assassin",
                    "Phantom Lancer", "Phoenix", "Puck", "Pudge", "Pugna", "Queen of Pain", "Razor", "Riki", "Rubick",
                    "Sand King", "Shadow Demon", "Shadow Fiend", "Shadow Shaman", "Silencer", "Skywrath Mage", "Slark",
                    "Slardar", "Snapfire", "Sniper", "Spectre", "Spirit Breaker", "Storm Spirit", "Sven", "Techies",
                    "Templar Assassin", "Terrorblade", "Tidehunter", "Timbersaw", "Tinker", "Tiny", "Treant Protector",
                    "Troll Warlord", "Tusk", "Underlord", "Undying", "Ursa", "Vengeful Spirit", "Venomancer", "Viper",
                    "Visage", "Void Spirit", "Warlock", "Weaver", "Windranger", "Winter Wyvern", "Witch Doctor",
                    "Wraith King", "Zues"]

        for x in range(len(heroList)):
            self.ui.heroSelectCombo.setItemText(x + 1, QCoreApplication.translate("MainWindow", heroList[x]))

        self.ui.amountSelectCombo.setItemText(0, QCoreApplication.translate("MainWindow", "Select Amount"))
        for x in range(1, 21):
            self.ui.amountSelectCombo.setItemText(x, QCoreApplication.translate("MainWindow", str(x)))
        self.ui.amountSelectCombo.setItemText(21, QCoreApplication.translate("MainWindow", "All"))

        self.ui.downloadButton.clicked.connect(self.downloadPressed)
        self.ui.browseButton.clicked.connect(browsePressed)
        # end local modifications to gui

    def downloadPressed(self):
        replaysList = getReplayFolderSnapshot()
        selectedHero = self.ui.heroSelectCombo.currentText().replace(" ", "%20")
        amount = int(self.ui.amountSelectCombo.currentText())

        # preparing options for chromedriver
        options = webdriver.ChromeOptions()
        options.add_argument('headless')

        browser = webdriver.Chrome(executable_path=os.getcwd() + "\\chromedriver.exe", options=options)

        # gets a list of the games played with the specified hero and a list of the playing
        # the hero, length both capped by the amount that the user has specified
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

            matchID = game.rsplit('/', 1)[-1]
            duplicate = False

            # if the replay attempting to be downloaded already exists
            # inside of the dota 2 replays folder, skip it
            for file in os.listdir(getReplaysDirectory()):
                if matchID in file:
                    print("Replay already downloaded!\n\n")
                    duplicate = True
                    break

            if duplicate is False:
                getReplay(game, browser)

            # updates the progress bar based on the amount of games
            downloadProgress += int((1 / gameAmount) * 100)
            self.ui.progressBar.setProperty("value", downloadProgress)
            QApplication.processEvents()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
