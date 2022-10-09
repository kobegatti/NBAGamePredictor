from bs4 import BeautifulSoup
import pandas as pd
import requests

url = "https://basketball.realgm.com/nba/team-stats"
filepath = 'data/2021-22.csv'

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

   tables = soup.find_all('table')
   table = tables[0]

   for row in table.tbody.find_all('tr'):
      columns = row.find_all('td')

      if (columns != []):
         name = columns[1].text.strip()
         gp = int(columns[2].text.strip())
         mpg = float(columns[3].text.strip())
         ppg = float(columns[4].text.strip())
         fgm = float(columns[5].text.strip())
         fga = float(columns[6].text.strip())
         fg_percent = float(columns[7].text.strip())
         threepm = float(columns[8].text.strip())
         threepa = float(columns[9].text.strip())
         three_percent = float(columns[10].text.strip())
         ftm = float(columns[11].text.strip())
         fta = float(columns[12].text.strip())
         ft_percent = float(columns[13].text.strip())
         orb = float(columns[14].text.strip())
         drb = float(columns[15].text.strip())
         rpg = float(columns[16].text.strip())
         apg = float(columns[17].text.strip())
         spg = float(columns[18].text.strip())
         bpg = float(columns[19].text.strip())
         tov = float(columns[20].text.strip())
         pf = float(columns[21].text.strip())
         
         df = pd.DataFrame({'Team': [name], 'GP': [gp], 
                            'MPG': [mpg], 'PPG': [ppg], 'FGM': [fgm], 
                            'FGA': [fga], 'FG%': [fg_percent], '3PM': [threepm],
                            '3PA': [threepa], '3P%': [three_percent], 'FTM': [ftm], 
                            'FTA': [fta], 'FT%': [ft_percent], 'ORB': [orb], 
                            'DRB': [drb], 'RPG': [rpg], 'APG': [apg], 
                            'SPG': [spg], 'BPG': [bpg], 'TOV': [tov], 'PF': [pf]})

         dataTable = pd.concat([dataTable, df], ignore_index=True)

   dataTable.to_csv(filepath)

