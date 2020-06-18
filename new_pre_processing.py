import pandas as pandas
from datetime import datetime


# season calculator
def get_season(date_string):
    date = datetime.strptime(date_string[:10], '%Y-%m-%d')
    if date.month >= 8:
        return date.year
    else:
        date = date - pandas.DateOffset(years=1)
        return date.year


# season fixer
def fix_season(date_string):
    return date_string[:4]


try:
    matches_data = pandas.read_csv('datasets/Match.csv')
    teams_data = pandas.read_csv('datasets/Team.csv')
except FileNotFoundError:
    matches_data = None
    teams_data = None



# Replace date with season's year
# print(matches_data)
#
#
# print(matches_data)

# matches_data.loc[:, 'home_player_1':'away_player_11'].replace(id, players_data)



