# Dota Pro Replay Downloader
  An application that downloads 'pro-level' Dota 2 replays of the specified hero to the Dota 2 replays directory.

  ## Summary
  This program takes data in the form of match id's of high mmr players from [dota2protracker.com](https://www.dota2protracker.com/) 
  for the hero the user has specified. The replays of the specific match id's are then grabbed from  [opendota.com](https://www.opendota.com/) 
  and installed into the directory of the users choice (which should be the location of their Dota 2 replays folder). The user can select 
  the hero they want to download replays of and how many they want to download. After downloading is complete, a summary of what replays 
  have been downloaded is shown. Duplicate replays (replays that have been requested to download but are already in the replays directory) 
  are skipped and the user is prompted.
  
  This program makes only one visit to [dota2protracker.com](https://www.dota2protracker.com/) per download request, regardless 
  of the download amount, so the traffic to the website is just as minimal as if the one downloading was visiting the site and downloading 
  replays personally. The same can be said for visits to [opendota.com](https://www.opendota.com/). Dota Pro Replay Downloader is just a tool 
  that preforms the same actions one would take to download replays manually, and should just be used as a time-saving replacement.
  
  ## Use
  Once opened, you should specify:
  - What directory to download replays to, usually located in 
  *Program Files (x86)\Steam\steamapps\common\dota 2 beta\game\dota\replays* 
  - The hero which you want to download replays of
  - The amount of replays you wish to download
  
  Then simply press *Download* to install the replays
  
  As a side note, one must still open the Dota 2 client and *download* the replays manually once they are in the replays directory.
  Unfortunately, match replays cannot be fully installed through means outside of the client.
  
  This does mean however, that space will not be taken up unnecessarily on your hard disk due to replays downloaded by the program, 
  as only the file name of the replay need be correct to have the client recognize it as a downloadable replay.
  In other words, until downloaded in-game, every replay downloaded through Dota Pro Replay Downloader are empty files and take up no space.
  
  That being said, Valve does set a time limit on replay acquisition: replays are only available for **8 days** after the game took place.
  So if one wants to store a watchable replay, they should download from the client before that time limit is reached.
  
  ## Installation
  (WIP)
  
  
***The GNU General Public License (located in [LICENSE.md](/LICENSE.md)) applies to all files in this repository.***
