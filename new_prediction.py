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
    train = data.loc[data.season != 2015]
    test = data.loc[data.season == 2015]
    train_predictors = train[predictors]
    train_target = train[outcome]
    # for i in range(0,10):
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


is_winner = lambda x: assign_winner(x)


# Fill NaN Bets
def fill_null_bet(data, column_name):
    data[column_name].fillna(data[column_name].mean(), inplace=True)


# Import Data - Match table
try:
    matches_data = pandas.read_csv('datasets/finalDataSet.csv')
except FileNotFoundError:
    _data = None
    raise FileNotFoundError

matches_data = matches_data[['country_id','league_id','season','stage','match_api_id','home_team_api_id','away_team_api_id',
                             'home_team_goal','away_team_goal','home_player_1','home_player_2','home_player_3','home_player_4','home_player_5','home_player_6',
                             'home_player_7','home_player_8','home_player_9','home_player_10','home_player_11','away_player_1',
                             'away_player_2','away_player_3','away_player_4','away_player_5','away_player_6','away_player_7',
                             'away_player_8','away_player_9','away_player_10','away_player_11',
'buildUpPlaySpeed_H', 'buildUpPlayDribbling_H', 'buildUpPlayPassing_H', 'defencePressure_H',
            'defenceTeamWidth_H',
            'defenceAggression_H',
            'chanceCreationShooting_H', 'chanceCreationPassing_H', 'chanceCreationCrossing_H',
            'buildUpPlaySpeed_A', 'buildUpPlayDribbling_A', 'buildUpPlayPassing_A', 'defencePressure_A',
            'defenceTeamWidth_A',
            'defenceAggression_A',
            'chanceCreationShooting_A', 'chanceCreationPassing_A', 'chanceCreationCrossing_A'
                             ]]

# Test Columns
test_mod = ['country_id','league_id','season','stage','home_team_api_id','away_team_api_id',
            'home_player_1','home_player_2','home_player_3','home_player_4','home_player_5','home_player_6',
             'home_player_7','home_player_8','home_player_9','home_player_10','home_player_11','away_player_1',
             'away_player_2','away_player_3','away_player_4','away_player_5','away_player_6','away_player_7',
             'away_player_8','away_player_9','away_player_10','away_player_11',
            'buildUpPlaySpeed_H', 'buildUpPlayDribbling_H', 'buildUpPlayPassing_H', 'defencePressure_H',
            'defenceTeamWidth_H',
            'defenceAggression_H',
            'chanceCreationShooting_H', 'chanceCreationPassing_H', 'chanceCreationCrossing_H',
            'buildUpPlaySpeed_A', 'buildUpPlayDribbling_A', 'buildUpPlayPassing_A', 'defencePressure_A',
            'defenceTeamWidth_A',
            'defenceAggression_A',
            'chanceCreationShooting_A', 'chanceCreationPassing_A', 'chanceCreationCrossing_A'
            ]
# mean_columns_nullVals = ['home_player_1','home_player_2','home_player_3','home_player_4','home_player_5','home_player_6',
#                              'home_player_7','home_player_8','home_player_9','home_player_10','home_player_11','away_player_1',
#                              'away_player_2','away_player_3','away_player_4','away_player_5','away_player_6','away_player_7',
#                              'away_player_8','away_player_9','away_player_10','away_player_11']
# for column in mean_columns_nullVals:
#     # if matches_data[column].dtype == "float64":
#     matches_data[column].fillna(matches_data[column].mean(), inplace=True)
# encoder = LabelEncoder()

# for column in test_mod:
#     fill_null_bet(_data, column)
#
# for i in var_mod:
#     _data[i] = encoder.fit_transform(_data[i])

matches_data['result'] = matches_data['home_team_goal'] - matches_data['away_team_goal']
matches_data['result'] = matches_data['result'].apply(is_winner)

# test_mod = ['season','home_player_1','home_player_2','home_player_3','home_player_4','home_player_5','home_player_6',
#              'home_player_7','home_player_8','home_player_9','home_player_10','home_player_11','away_player_1',
#              'away_player_2','away_player_3','away_player_4','away_player_5','away_player_6','away_player_7',
#              'away_player_8','away_player_9','away_player_10','away_player_11']
# RF Classifier
outcome_var = 'result'
_model = RandomForestClassifier(n_estimators=100, min_samples_split=100, max_depth=30, max_features='auto')
classification_model(_model, matches_data, test_mod, outcome_var)
