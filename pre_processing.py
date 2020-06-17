import pandas as pandas

try:
    _data = pandas.read_csv('datasets/Match.csv')
except FileNotFoundError:
    _data = None

# All Bet Data columns
bet_columns = ['B365H', 'B365D', 'B365A', 'BWH', 'BWD', 'BWA', 'IWH', 'IWD', 'IWA', 'LBH',
               'LBD', 'LBA', 'WHH', 'WHD', 'WHA', 'SJH', 'SJD', 'SJA', 'VCH', 'VCD', 'VCA',
               'GBH', 'GBD', 'GBA', 'BSH', 'BSD', 'BSA', 'PSH', 'PSD', 'PSA']
# Home win chances
bet_columns_H = ['B365H', 'BWH', 'IWH',  'LBH', 'WHH', 'SJH', 'VCH', 'GBH', 'BSH', 'PSH']
# Draw chances
bet_columns_D = ['B365D', 'BWD', 'IWD',  'LBD', 'WHD', 'SJD', 'VCD', 'GBD', 'BSD', 'PSD']
# Away win chances
bet_columns_A = ['B365A', 'BWA', 'IWA',  'LBA', 'WHA', 'SJA', 'VCA', 'GBA', 'BSA', 'PSA']

# Data Preparation
cleaned_data_frame = []
for index, row in _data.iterrows():
    if row[bet_columns].isna().sum() < len(bet_columns):
        cleaned_data_frame.append(index)
        if row[bet_columns].isna().sum() > 0:
            avg_A = row[bet_columns_A].sum()/row[bet_columns_A].isna().sum()
            avg_D = row[bet_columns_D].sum()/row[bet_columns_D].isna().sum()
            avg_H = row[bet_columns_H].sum()/row[bet_columns_H].isna().sum()
            for column in bet_columns_A:
                if _data[index:index+1][column].isna().sum() != 0:
                    _data[index:index+1][column].fillna(avg_A, inplace=True)
            for column in bet_columns_D:
                if _data[index:index + 1][column].isna().sum() != 0:
                    _data[index:index+1][column].fillna(avg_D, inplace=True)
            for column in bet_columns_H:
                if _data[index:index+1][column].isna().sum() != 0:
                    _data[index:index + 1][column].fillna(avg_H, inplace=True)
_data = _data.loc[cleaned_data_frame]
print(_data)
# Save new data csv
_data.to_csv('datasets/Match_cleaned.csv')
