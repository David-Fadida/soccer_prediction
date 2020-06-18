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


def fix_season(season):
    return season[0:4]


def getOverall(table , player_id , season):
    try:
        player_id = int(player_id)
        season = int(season)
    except ValueError:
        return None
    try:
        return round(table.get_group((player_id,season)).mean()['overall_rating'])
    except Exception as e:
        return None


pandas.set_option('mode.chained_assignment', None)

try:
    matches_data = pandas.read_csv('datasets/Match.csv')
    teams_data = pandas.read_csv('datasets/Team.csv')
    player_data = pandas.read_csv('datasets/Player.csv')
except FileNotFoundError:
    matches_data = None
    teams_data = None
    player_data = None

matches_data = matches_data[['country_id','league_id','season','stage','match_api_id','home_team_api_id','away_team_api_id',
                             'home_team_goal','away_team_goal','home_player_1','home_player_2','home_player_3','home_player_4','home_player_5','home_player_6',
                             'home_player_7','home_player_8','home_player_9','home_player_10','home_player_11','away_player_1',
                             'away_player_2','away_player_3','away_player_4','away_player_5','away_player_6','away_player_7',
                             'away_player_8','away_player_9','away_player_10','away_player_11']]
player_fields = ['home_player_1','home_player_2','home_player_3','home_player_4','home_player_5','home_player_6',
                  'home_player_7','home_player_8','home_player_9','home_player_10','home_player_11','away_player_1',
                  'away_player_2','away_player_3','away_player_4','away_player_5','away_player_6','away_player_7',
                  'away_player_8','away_player_9','away_player_10','away_player_11']
matches_data['season'] = matches_data['season'].apply(lambda x: fix_season(x))

seasons = player_data['date'].apply(lambda x: get_season(x))
player_df = pandas.DataFrame(data= player_data[['player_api_id','overall_rating']])
player_df = player_df.assign(seasons=seasons)
group_data=player_df.groupby(['player_api_id','seasons'])

for index, row in matches_data[950:1000].iterrows():
    for column in player_fields:
        matches_data[index:index+1][column] = getOverall(group_data ,matches_data[index:index+1][column],
                                                         matches_data[index:index + 1]['season'])
print(matches_data[950:1000]['home_player_1'])
matches_data.to_csv('datasets/playersDataCombined.csv')

#
#  TEAMS DATA
#

attributes = ['team_api_id', 'seasons', 'buildUpPlaySpeed', 'buildUpPlayDribbling',
              'buildUpPlayPassing', 'defencePressure', 'defenceTeamWidth', 'defenceAggression',
              'chanceCreationShooting', 'chanceCreationPassing', 'chanceCreationCrossing']

seasons = teams_data['date'].apply(lambda x: get_season(x))
teams_data = teams_data.assign(seasons=seasons)
teams_data = pandas.DataFrame(data=teams_data[attributes])

teams_data = teams_data.groupby(['team_api_id', 'seasons'], as_index=False).mean()
matches_data['season'] = matches_data['season'].astype(str).astype(int)

# Add HOME team attributes
for att in attributes:
    teams_data.rename(columns={att: att+'_H'}, inplace=True)
data = matches_data.merge(
    teams_data,
    how='left',
    left_on=['home_team_api_id', 'season'],
    right_on=['team_api_id_H', 'seasons_H']
)

# Add AWAY team attributes
for att in attributes:
    teams_data.rename(columns={att+'_H': att+'_A'}, inplace=True)
data = data.merge(
    teams_data,
    how='left',
    left_on=['away_team_api_id', 'season'],
    right_on=['team_api_id_A', 'seasons_A']
)

# Save new data csv
data.to_csv('datasets/tempDataSet.csv')

fill_na = ['home_player_1','home_player_2','home_player_3','home_player_4','home_player_5','home_player_6', 'home_player_7','home_player_8',
           'home_player_9','home_player_10','home_player_11','away_player_1','away_player_2','away_player_3','away_player_4','away_player_5',
           'away_player_6','away_player_7', 'away_player_8','away_player_9','away_player_10','away_player_11',
           'buildUpPlaySpeed_H', 'buildUpPlayDribbling_H','buildUpPlayPassing_H', 'defencePressure_H', 'defenceTeamWidth_H',
           'defenceAggression_H',
           'chanceCreationShooting_H', 'chanceCreationPassing_H', 'chanceCreationCrossing_H',
           'buildUpPlaySpeed_A', 'buildUpPlayDribbling_A', 'buildUpPlayPassing_A', 'defencePressure_A',
           'defenceTeamWidth_A',
           'defenceAggression_A',
           'chanceCreationShooting_A', 'chanceCreationPassing_A', 'chanceCreationCrossing_A']

for column in fill_na:
    data[column].fillna(data[column].mean(), inplace=True)

# Save new data csv
data.to_csv('datasets/finalDataSet.csv')
