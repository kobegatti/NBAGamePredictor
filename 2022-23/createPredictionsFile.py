# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 16:24:00 2022

@author: kobeg
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

if __name__ == '__main__':
    filePath = "data/2022-23Predictions.csv"
    url = "https://www.basketball-reference.com/leagues/NBA_2023.html"
    
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    
    dataTable = pd.DataFrame(data={'Team': [], 'Predicted_W': [], 'Predicted_L': [],
                                   'Predicted_Total': [], 'Error_Rate': []})
    
    tr_elements = soup.find("table", {"id" : "confs_standings_E"}).find_all('tr')     
    
    for row in tr_elements:
        columns = row.find_all()
        
        if columns != [] and len(columns[1].text.strip()) > 1:
            teamName = columns[1].text.strip()
            actual_wins = int(columns[2].text.strip().replace("(", "").replace(")", ""))
            actual_losses = int(columns[3].text.strip().replace("(", "").replace(")", ""))
            
            df = pd.DataFrame({'Team': [teamName], 'Predicted_W': [0], 
                               'Predicted_L': [0], 'Predicted_Total': [0], 
                               'Error_Rate': [0]})
            
            dataTable = pd.concat([dataTable, df], ignore_index=True)
        

    tr_elements = soup.find("table", {"id" : "confs_standings_W"}).find_all('tr')
    
    for row in tr_elements:
        columns = row.find_all()
        
        if columns != [] and len(columns[1].text.strip()) > 1:
            teamName = columns[1].text.strip()
            actual_wins = int(columns[2].text.strip().replace("(", "").replace(")", ""))
            actual_losses = int(columns[3].text.strip().replace("(", "").replace(")", ""))
            
            df = pd.DataFrame({'Team': [teamName], 'Predicted_W': [0], 
                               'Predicted_L': [0], 'Predicted_Total': [0], 
                               'Error_Rate': [0]})
            
            dataTable = pd.concat([dataTable, df], ignore_index=True)
    
    
    dataTable.to_csv(filePath)