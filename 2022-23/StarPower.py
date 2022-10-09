# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 23:03:21 2022

@author: kobeg
"""

import json
from pathlib import Path
from bs4 import BeautifulSoup
import requests

dir_name = 'data'
file_name = 'starPower.json'

star_power = {"Minnesota": 55,
              "Memphis": 55,
              "Milwaukee": 55,
              "Charlotte": 55,
              "Phoenix": 55,
              "Atlanta": 55,
              "Utah": 55,
              "San Antonio": 55,
              "Brooklyn": 55,
              "Denver": 55,
              "L.A. Lakers": 55,
              "Boston": 55,
              "Chicago": 55,
              "Indiana": 55,
              "Golden State": 55,
              "Sacramento": 55,
              "Miami": 55,
              "Philadelphia": 55,
              "Houston": 55,
              "Toronto": 55,
              "New Orleans": 55,
              "Washington": 55,
              "L.A. Clippers": 55,
              "Dallas": 55,
              "Cleveland": 55,
              "New York": 55,
              "Portland": 55,
              "Detroit": 55,
              "Orlando": 55,
              "Oklahoma City": 55
             }

AllStar = 'AllStar'
all_star_url = 'https://basketball.realgm.com/nba/allstar/game/rosters'

RisingStar = 'RisingStar'
rising_star_url = 'https://basketball.realgm.com/nba/allstar/rising_stars_challenge/rosters'

ThreePt = 'ThreePt'
three_pt_url = 'https://basketball.realgm.com/nba/allstar/three_point/selections_by_season'

Skills = 'Skills'
skills_url = 'https://basketball.realgm.com/nba/allstar/skills/selections_by_season'

SlamDunk = 'SlamDunk'
slam_dunk_url = 'https://basketball.realgm.com/nba/allstar/dunk/selections_by_season'


def incrementDictEntry(Team, Value):
    if (Team.find("Minnesota") >= 0):
        star_power["Minnesota"] += Value
    elif (Team.find("Memphis") >= 0):
        star_power["Memphis"] += Value
    elif (Team.find("Milwaukee") >= 0):
        star_power["Milwaukee"] += Value
    elif (Team.find("Charlotte") >= 0):
        star_power["Charlotte"] += Value
    elif (Team.find("Phoenix") >= 0):
        star_power["Phoenix"] += Value
    elif (Team.find("Atlanta") >= 0):
        star_power["Atlanta"] += Value
    elif (Team.find("Utah") >= 0):
        star_power["Utah"] += Value
    elif (Team.find("San Antonio") >= 0):
        star_power["San Antonio"] += Value
    elif (Team.find("Brooklyn") >= 0):
        star_power["Brooklyn"] += Value
    elif (Team.find("Denver") >= 0):
        star_power["Denver"] += Value
    elif (Team.find("Lakers") >= 0):
        star_power["L.A. Lakers"] += Value
    elif (Team.find("Boston") >= 0):
        star_power["Boston"] += Value
    elif (Team.find("Chicago") >= 0):
        star_power["Chicago"] += Value
    elif (Team.find("Indiana") >= 0):
        star_power["Indiana"] += Value
    elif (Team.find("Golden State") >= 0):
        star_power["Golden State"] += Value
    elif (Team.find("Sacramento") >= 0):
        star_power["Sacramento"] += Value
    elif (Team.find("Miami") >= 0):
        star_power["Miami"] += Value
    elif (Team.find("Philadelphia") >= 0):
        star_power["Philadelphia"] += Value
    elif (Team.find("Houston") >= 0):
        star_power["Houston"] += Value
    elif (Team.find("Houston") >= 0):
        star_power["Milwaukee"] += Value
    elif (Team.find("Toronto") >= 0):
        star_power["Toronto"] += Value
    elif (Team.find("New Orleans") >= 0):
        star_power["New Orleans"] += Value
    elif (Team.find("Washington") >= 0):
        star_power["Washington"] += Value
    elif (Team.find("Clippers") >= 0):
        star_power["L.A. Clippers"] += Value
    elif (Team.find("Dallas") >= 0):
        star_power["Dallas"] += Value
    elif (Team.find("Cleveland") >= 0):
        star_power["Cleveland"] += Value
    elif (Team.find("New York") >= 0):
        star_power["New York"] += Value
    elif (Team.find("Portland") >= 0):
        star_power["Portland"] += Value
    elif (Team.find("Detroit") >= 0):
        star_power["Detroit"] += Value
    elif (Team.find("Orlando") >= 0):
        star_power["Orlando"] += Value
    elif (Team.find("Oklahoma City") >= 0):
        star_power["Oklahoma City"] += Value


def calculatePower(url, powerType):
    increment = 0
    
    if (powerType == AllStar):
        increment = 21
    elif (powerType == RisingStar):
        increment = 13
    elif (powerType == ThreePt):
        increment = 5
    elif (powerType == Skills):
        increment = 2
    elif (powerType == SlamDunk):
        increment = 1
    
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')
    
    tables = soup.find_all("table", attrs={"class": "basketball compact"})
    
    for table in tables:
        tr_elements = table.find_all('tr')
        
        for row in tr_elements:
            columns = row.find_all('td')
            
            if columns != []:
                team_name = columns[4].text.strip()
                incrementDictEntry(team_name, increment)
        
        
if __name__ == '__main__':
    base = Path(dir_name)
    base.mkdir(exist_ok=True)
    
    team_with_MVP = 'Denver'
    star_power[team_with_MVP] += 34
    
    calculatePower(all_star_url, AllStar)
    calculatePower(rising_star_url, RisingStar)
    calculatePower(three_pt_url, ThreePt)
    calculatePower(skills_url, Skills)
    calculatePower(slam_dunk_url, SlamDunk)
    
    filepath = base / (file_name)
    filepath.write_text(json.dumps(star_power))