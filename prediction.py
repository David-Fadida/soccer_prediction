import numpy as numpy
import pandas as pandas

from sklearn import metrics
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


# Classification Model Function
def classification_model(model, data, predictors, outcome):
    model.fit(data[predictors], data[outcome])
    predictions = model.predict(data[predictors])
    accuracy = metrics.accuracy_score(predictions, data[outcome])
    print("Training accuracy : %s" % "{0: .3%}".format(accuracy))
    accuracy = []
    train = data.loc[data.season != '2015/2016']
    # train = train[0]
    print(train)
    test = data.loc[data.season == '2015/2016']
    train_predictors = train[predictors]
    train_target = train[outcome]
    model.fit(train_predictors, train_target)
    accuracy.append(model.score(test[predictors], test[outcome]))
    print("Cross-Validation-Score : %s" % "{0: .3%}".format(numpy.mean(accuracy)))
    model.fit(data[predictors], data[outcome])


# Assign Winner
def assign_winner(game_result):
    if game_result < 0:
        return -1
    elif game_result > 0:
        return 1
    else:
        return 0


# LAMBDA Assign Winner
is_winner = lambda x: assign_winner(x)


# Fill NaN Bets
def fill_null_bet(data, column_name):
    data[column_name].fillna(data[column_name].mean(), inplace=True)


# Import Data - Match table
try:
    _data = pandas.read_csv('datasets/Match.csv')
except FileNotFoundError:
    _data = None
    var_mod = None
    test_mod = None
    encoder = None
else:
    var_mod = ['id', 'league_id', 'season', 'home_team_api_id', 'away_team_api_id', 'home_team_goal', 'away_team_goal',
               'home_player_1', 'home_player_2', 'home_player_3', 'home_player_4', 'home_player_5', 'home_player_6',
               'home_player_7', 'home_player_8', 'home_player_9', 'home_player_10', 'home_player_11', 'away_player_1',
               'away_player_2', 'away_player_3', 'away_player_4', 'away_player_5', 'away_player_6', 'away_player_7',
               'away_player_8', 'away_player_9', 'away_player_10', 'away_player_11', 'B365H', 'B365D', 'B365A', 'BWH',
               'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'LBH', 'LBD', 'LBA', 'WHH', 'WHD', 'WHA', 'SJH', 'SJD', 'SJA', 'VCH',
               'VCD', 'VCA', 'GBH', 'GBD', 'GBA', 'BSH', 'BSD', 'BSA']
    test_mod = ['home_team_api_id', 'away_team_api_id', 'B365H', 'B365D', 'B365A']
    encoder = LabelEncoder()

# Data Preparation
for column in test_mod:
    fill_null_bet(_data, column)

# for i in var_mod:
#     _data[i] = encoder.fit_transform(_data[i])

new_column = _data['home_team_goal'] - _data['away_team_goal']
_data = _data.assign(result=new_column)
_data['result'] = _data['result'].apply(is_winner)

# RF Classifier
outcome_var = 'result'
_model = RandomForestClassifier(n_estimators=100)
classification_model(_model, _data, test_mod, outcome_var)
