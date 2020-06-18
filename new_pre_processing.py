import pandas as pandas
from datetime import datetime


# season calculator
def get_season(date_string):
    date = datetime.strptime(date_string[:9], '%Y-%m-%d')
    if date.month >= 8:
        return date.year
    else:
        date = date - pandas.DateOffset(years=1)
        return date.year


print(get_season('2011-02-22 00:00:00'))
print(get_season('2014-09-19 00:00:00'))
print(get_season('2013-09-20 00:00:00'))

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

# Save new data csv
# matches_data.to_csv('datasets/Match_Cleaned_New.csv')

