# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 23:25:57 2022

@author: kobeg
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
filepath = 'data/2022-23.csv'

if __name__ == '__main__':
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')

    dataTable = pd.DataFrame(data={'Team': [], 'GP': [], 'MPG': [], 
                                   'PPG': [], 'FGM': [], 'FGA': [], 
                                   'FG%': [], '3PM': [], '3PA': [], 
                                   '3P%': [], 'FTM': [], 'FTA': [], 
                                   'FT%': [], 'ORB': [], 'DRB': [], 
                                   'RPG': [], 'APG': [], 'SPG': [], 
                                   'BPG': [], 'TOV': [], 'PF': []})

    tables = soup.find("table", {"class" : "stats_table sortable",
                                 "id" : "per_game-team"})
    
    tr_elements = soup.find("table", {"class" : "stats_table sortable",
                                 "id" : "per_game-team"}).find_all('tr')
    
    for row in tr_elements:
        columns = row.find_all('td')

        if (columns != []):
            name = columns[0].text.strip()
            gp = int(0 if columns[1].text.strip() == '' else columns[1].text.strip())
            mpg = float(0 if columns[2].text.strip() == '' else columns[2].text.strip())
            fgm = float(0 if columns[3].text.strip() == '' else columns[3].text.strip())
            fga = float(0 if columns[4].text.strip() == '' else columns[4].text.strip())
            fg_percent = float(0 if columns[5].text.strip() == '' else columns[5].text.strip())
            threepm = float(0 if columns[6].text.strip() == '' else columns[6].text.strip())
            threepa = float(0 if columns[7].text.strip() == '' else columns[7].text.strip())
            three_percent = float(0 if columns[8].text.strip() == '' else columns[8].text.strip())
            ftm = float(0 if columns[12].text.strip() == '' else columns[12].text.strip())
            fta = float(0 if columns[13].text.strip() == '' else columns[13].text.strip())
            ft_percent = float(0 if columns[14].text.strip() == '' else columns[14].text.strip())
            orb = float(0 if columns[15].text.strip() == '' else columns[15].text.strip())
            drb = float(0 if columns[16].text.strip() == '' else columns[16].text.strip())
            rpg = float(0 if columns[17].text.strip() == '' else columns[17].text.strip())
            apg = float(0 if columns[18].text.strip() == '' else columns[18].text.strip())
            spg = float(0 if columns[19].text.strip() == '' else columns[19].text.strip())
            bpg = float(0 if columns[20].text.strip() == '' else columns[20].text.strip())
            tov = float(0 if columns[21].text.strip() == '' else columns[21].text.strip())
            pf = float(0 if columns[22].text.strip() == '' else columns[22].text.strip())
            ppg = float(0 if columns[23].text.strip() == '' else columns[23].text.strip())
            
            df = pd.DataFrame({'Team': [name], 'GP': [gp], 
                               'MPG': [mpg], 'PPG': [ppg], 'FGM': [fgm], 
                               'FGA': [fga], 'FG%': [fg_percent], '3PM': [threepm],
                               '3PA': [threepa], '3P%': [three_percent], 'FTM': [ftm], 
                               'FTA': [fta], 'FT%': [ft_percent], 'ORB': [orb], 
                               'DRB': [drb], 'RPG': [rpg], 'APG': [apg], 
                               'SPG': [spg], 'BPG': [bpg], 'TOV': [tov], 'PF': [pf]})

            dataTable = pd.concat([dataTable, df], ignore_index=True)
    
    dataTable.to_csv(filepath)