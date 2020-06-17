import pandas as pandas

try:
    matches_data = pandas.read_csv('datasets/Match.csv')
    players_data = pandas.read_csv('datasets/Player.csv')
except FileNotFoundError:
    matches_data = None
    players_data = None

#
#   TO DO : new algorithm - old one didn't work
#

matches_data.replace()
print(matches_data)
# Save new data csv
matches_data.to_csv('datasets/Match_Cleaned_New.csv')

