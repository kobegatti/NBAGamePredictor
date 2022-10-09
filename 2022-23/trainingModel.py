# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 21:51:41 2022

@author: kobeg
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
from random import randrange
import time

statsURL = "https://www.basketball-reference.com/leagues/NBA_2022.html"
records = 'data/2021-22_WL_records.csv'

lastSeasonPath = 'data/2021-22.csv'
thisSeasonPath = 'data/2022-23.csv'

starPowerPath = 'data\starPower.json'

playoffsStart = 'Apr 12'

TOTAL_GAMES = 82

schedule = ["https://www.basketball-reference.com/leagues/NBA_2022_games-october.html",
            "https://www.basketball-reference.com/leagues/NBA_2022_games-november.html",
            "https://www.basketball-reference.com/leagues/NBA_2022_games-december.html",
            "https://www.basketball-reference.com/leagues/NBA_2022_games-january.html",
            "https://www.basketball-reference.com/leagues/NBA_2022_games-february.html",
            "https://www.basketball-reference.com/leagues/NBA_2022_games-march.html",
            "https://www.basketball-reference.com/leagues/NBA_2022_games-april.html"]

weights = {"3P%" : .33,
           "PPG" : .05,
           "APG" : .10,
           "TOV" : -.19,
           "RPG" : .12,
           "FG%" : .16, 
           "SPG" : .03,
           "BPG" : .02}
# -0.03
'''
weights = {"3P%" : .33,
           "PPG" : .05,
           "APG" : .10,
           "TOV" : -.19,
           "RPG" : .12,
           "FG%" : .16, 
           "SPG" : .03,
           "BPG" : .02}

weights = {"3P%" : .33,
           "PPG" : .05,
           "APG" : .11,
           "TOV" : -.19,
           "RPG" : .11,
           "FG%" : .17, 
           "SPG" : .03,
           "BPG" : .01}
'''

def getActualRecords(filePath):
    data = requests.get(statsURL).text
    soup = BeautifulSoup(data, 'html.parser')
    
    dataTable = pd.DataFrame(data={'Team': [], 'Actual_W': [], 'Actual_L': [], 
                                   'Predicted_W': [], 'Predicted_L': [],
                                   'Predicted_Total': [], 'Error_Rate': []})
    
    tr_elements = soup.find("table", {"id" : "confs_standings_E"}).find_all('tr')
    
    for row in tr_elements:
        columns = row.find_all()
        
        if columns != [] and len(columns[1].text.strip()) > 1:
            teamName = columns[1].text.strip()
            actual_wins = int(columns[2].text.strip())
            actual_losses = int(columns[3].text.strip())
            
            df = pd.DataFrame({'Team': [teamName], 'Actual_W': [actual_wins],
                              'Actual_L': [actual_losses], 'Predicted_W': [0],
                              'Predicted_L': [0], 'Predicted_Total': [0], 
                              'Error_Rate': [0]})
            
            dataTable = pd.concat([dataTable, df], ignore_index=True)
            
    
    tr_elements = soup.find("table", {"id" : "confs_standings_W"}).find_all('tr')
    
    for row in tr_elements:
        columns = row.find_all()
        
        if columns != [] and len(columns[1].text.strip()) > 1:
            teamName = columns[1].text.strip()
            actual_wins = int(columns[2].text.strip())
            actual_losses = int(columns[3].text.strip())
            
            df = pd.DataFrame({'Team': [teamName], 'Actual_W': [actual_wins],
                              'Actual_L': [actual_losses], 'Predicted_W': [0],
                              'Predicted_L': [0], 'Predicted_Total': [0], 
                              'Error_Rate': [0]})
            
            dataTable = pd.concat([dataTable, df], ignore_index=True)
    
    
    dataTable.to_csv(records)
    

def getTeamName(name):
    teamName = ''
    
    if name.find("Lakers") >= 0 or name.find("Clippers") >= 0:
        teamName = "L.A. " + name.rsplit(' ', 1)[len(name.rsplit(' ', 1)) - 1]
    elif name.find("Portland") >= 0:
        teamName = name.split(' ')[0]
    else:
        teamName = name.rsplit(' ', 1)[0]
        
    return teamName


def getTeamStats(dataFrame, teamName):
    index = 0
    ret_val = []
    
    filtered = dataFrame['Team']
    
    for name in filtered:
        if (name.find(teamName) >= 0):
            ret_val = dataFrame.iloc[[index]]
        
        index += 1
        
    return ret_val


def calculate(recordsData, awayTeam, awayLastSeason, awayThisSeason, 
                  homeTeam, homeLastSeason, homeThisSeason, starPower):
    awayName = getTeamName(awayTeam)
    homeName = getTeamName(homeTeam)
    
    awayLastScore = (weights.get("3P%") * float(awayThisSeason.loc[awayThisSeason['Team'] == awayTeam, '3P%'])
                     + weights.get("PPG") * float(awayThisSeason.loc[awayThisSeason['Team'] == awayTeam, 'PPG'])
                     + weights.get("APG") * float(awayThisSeason.loc[awayThisSeason['Team'] == awayTeam, 'APG'])
                     + weights.get("TOV") * float(awayThisSeason.loc[awayThisSeason['Team'] == awayTeam, 'TOV'])
                     + weights.get("SPG") * float(awayThisSeason.loc[awayThisSeason['Team'] == awayTeam, 'SPG'])
                     + weights.get("RPG") * float(awayThisSeason.loc[awayThisSeason['Team'] == awayTeam, 'RPG'])
                     + weights.get("FG%") * float(awayThisSeason.loc[awayThisSeason['Team'] == awayTeam, 'FG%'])
                     + weights.get("BPG") * float(awayThisSeason.loc[awayThisSeason['Team'] == awayTeam, 'BPG']))
    
    awayThisScore = (weights.get("3P%") * float(awayLastSeason.loc[awayLastSeason['Team'] == awayName, '3P%'])
                     + weights.get("PPG") * float(awayLastSeason.loc[awayLastSeason['Team'] == awayName, 'PPG'])
                     + weights.get("APG") * float(awayLastSeason.loc[awayLastSeason['Team'] == awayName, 'APG'])
                     + weights.get("TOV") * float(awayLastSeason.loc[awayLastSeason['Team'] == awayName, 'TOV'])
                     + weights.get("SPG") * float(awayLastSeason.loc[awayLastSeason['Team'] == awayName, 'SPG'])
                     + weights.get("RPG") * float(awayLastSeason.loc[awayLastSeason['Team'] == awayName, 'RPG'])
                     + weights.get("FG%") * float(awayLastSeason.loc[awayLastSeason['Team'] == awayName, 'FG%'])
                     + weights.get("BPG") * float(awayLastSeason.loc[awayLastSeason['Team'] == awayName, 'BPG']))
    
                    
    
    homeLastScore = (weights.get("3P%") * float(homeLastSeason.loc[homeLastSeason['Team'] == homeName, '3P%'])
                     + weights.get("PPG") * float(homeLastSeason.loc[homeLastSeason['Team'] == homeName, 'PPG'])
                     + weights.get("APG") * float(homeLastSeason.loc[homeLastSeason['Team'] == homeName, 'APG'])
                     + weights.get("TOV") * float(homeLastSeason.loc[homeLastSeason['Team'] == homeName, 'TOV'])
                     + weights.get("SPG") * float(homeLastSeason.loc[homeLastSeason['Team'] == homeName, 'SPG'])
                     + weights.get("RPG") * float(homeLastSeason.loc[homeLastSeason['Team'] == homeName, 'RPG'])
                     + weights.get("FG%") * float(homeLastSeason.loc[homeLastSeason['Team'] == homeName, 'FG%'])
                     + weights.get("BPG") * float(homeLastSeason.loc[homeLastSeason['Team'] == homeName, 'BPG']))
    
    homeThisScore = (weights.get("3P%") * float(homeThisSeason.loc[homeThisSeason['Team'] == homeTeam, '3P%'])
                     + weights.get("PPG") * float(homeThisSeason.loc[homeThisSeason['Team'] == homeTeam, 'PPG'])
                     + weights.get("APG") * float(homeThisSeason.loc[homeThisSeason['Team'] == homeTeam, 'APG'])
                     + weights.get("TOV") * float(homeThisSeason.loc[homeThisSeason['Team'] == homeTeam, 'TOV'])
                     + weights.get("SPG") * float(homeThisSeason.loc[homeThisSeason['Team'] == homeTeam, 'SPG'])
                     + weights.get("RPG") * float(homeThisSeason.loc[homeThisSeason['Team'] == homeTeam, 'RPG'])
                     + weights.get("FG%") * float(homeThisSeason.loc[homeThisSeason['Team'] == homeTeam, 'FG%'])
                     + weights.get("BPG") * float(homeThisSeason.loc[homeThisSeason['Team'] == homeTeam, 'BPG']))
    
    
    awayTotalScore = float(0.5 * awayThisScore) + float(0.3 * awayLastScore) + float(0.2 * (starPower.get(awayName) + randrange(0, 54))) # 60 54
    homeTotalScore = float(0.5 * homeLastScore) + float(0.3 * homeThisScore) + float(0.2 * (starPower.get(homeName) + randrange(47, 101))) # 43 47
    
    
    if (homeTotalScore > awayTotalScore):
        # increment homePredictedWinColumn in records
        # increment awayPredictedLossColumn in records
        recordsData.loc[recordsData['Team'] == homeTeam, 'Predicted_W'] += 1
        recordsData.loc[recordsData['Team'] == awayTeam, 'Predicted_L'] += 1
    elif (awayTotalScore > homeTotalScore):
        # increment awayPredictedWinColumn in records
        # increment homePredictedLossColumn in records
        recordsData.loc[recordsData['Team'] == awayTeam, 'Predicted_W'] += 1
        recordsData.loc[recordsData['Team'] == homeTeam, 'Predicted_L'] += 1
    else:
        if (float(starPower.get(homeName)) >= float(starPower.get(awayName))):
            # increment homePredictedWinColumn in records
            # increment awayPredictedLossColumn in records
            recordsData.loc[recordsData['Team'] == homeTeam, 'Predicted_W'] += 1
            recordsData.loc[recordsData['Team'] == awayTeam, 'Predicted_L'] += 1
        else:
            # increment awayPredictedWinColumn in records
            # increment homePredictedLossColumn in records
            recordsData.loc[recordsData['Team'] == awayTeam, 'Predicted_W'] += 1
            recordsData.loc[recordsData['Team'] == homeTeam, 'Predicted_L'] += 1
        
    
    
def predict():
    records_data = pd.read_csv(records)
    last_season_data = pd.read_csv(lastSeasonPath)
    this_season_data = pd.read_csv(thisSeasonPath)
    
    f = open(starPowerPath)
    starPower = json.load(f)
    f.close()
    
    for month in schedule:
        data = requests.get(month).text
        soup = BeautifulSoup(data, 'html.parser')
        
        tr_elements = soup.find("table", {"id" : "schedule"}).find_all('tr')
        
        for row in tr_elements:
            columns = row.find_all()
            
            if (columns != []) and (columns[0].text.strip() != "Date"):
                
                if (columns[1].text.strip().find(playoffsStart) >= 0):
                    break
                
                #print(columns[1].text.strip())
                awayTeam = columns[3].text.strip()
                awayLastSeason = getTeamStats(last_season_data, 
                                            getTeamName(awayTeam))
                awayThisSeason = getTeamStats(this_season_data, 
                                            awayTeam)
                #print(awayTeam)
                #print(awayThisSeason)
                
                homeTeam = columns[6].text.strip()
                homeLastSeason = getTeamStats(last_season_data, 
                                            getTeamName(homeTeam))
                homeThisSeason = getTeamStats(this_season_data, 
                                            homeTeam)
                
                #print(awayTeam)
                #print(awayLastSeason)
                #print(awayThisSeason)
                
                #rint("\n")
                #print(homeTeam)
                #print(homeLastSeason)
                #print(homeThisSeason)
                
                calculate(records_data, awayTeam, awayLastSeason, awayThisSeason, 
                              homeTeam, homeLastSeason, homeThisSeason, starPower)
        
    for i in range(len(records_data.index)):
        records_data.loc[i, 'Predicted_Total'] = records_data.loc[i, 'Predicted_W'] + records_data.loc[i, 'Predicted_L']
        records_data.loc[i, 'Error_Rate'] = float(abs(records_data.loc[i, 'Predicted_W'] - records_data.loc[i, 'Actual_W']) / TOTAL_GAMES)
    
    print("Error Rate:", records_data['Error_Rate'].mean())
    records_data.to_csv(records)

if __name__ == '__main__':
    
    start = time.time()
    
    getActualRecords(records)
    
    predict()
    
    end = time.time()
    
    print("Executed in", end - start, "seconds")