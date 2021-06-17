import csv
import copy
import numpy as np
import matplotlib.pyplot as plt


def draw(average_testing_likes_by_date, average_non_testing_likes_by_date):
    xs = np.arange(len(average_testing_likes_by_date))

    testing_amount = []
    for key, value in average_testing_likes_by_date.items():
        testing_amount.append(value)

    non_testing_amount = []
    for key, value in average_non_testing_likes_by_date.items():
        non_testing_amount.append(value)

    series1 = np.array(testing_amount).astype(np.double)
    s1mask = np.isfinite(series1)
    series2 = np.array(non_testing_amount).astype(np.double)
    s2mask = np.isfinite(series2)

    plt.plot(xs[s1mask], series1[s1mask], linestyle='-', marker='o')
    plt.plot(xs[s2mask], series2[s2mask], linestyle='-', marker='o')

    plt.show()


def after_test_begin(row):
    tmp = row[4]
    return tmp in ['24.03.2017', '25.03.2017', '26.03.2017', '27.03.2017']


def desktop(row):
    tmp = row[1]
    return tmp == '6'


def mobile(row):
    tmp = row[1]
    return tmp == '7'


def male(row):
    tmp = row[3]
    return tmp == 'm'


def female(row):
    tmp = row[3]
    return tmp == 'f'


def read_data_from_csv(file_name):
    with open(file_name) as f:
        it = csv.reader(f, delimiter=';')
        data = []
        for row in it:
            if not after_test_begin(row):
                data.append(row)

    return data[1:10000]


def get_ids_by_dates(data):
    ids_by_dates = {}

    for row in data:
        key = row[2].split()[0]
        value = ids_by_dates.get(key)
        if value is None:
            value = []
        value.append(row[0])
        ids_by_dates[key] = value

    return ids_by_dates


_file_name = "AB_test_rawdata.csv"

_data = read_data_from_csv(_file_name)
_ids_by_dates = dict(sorted(get_ids_by_dates(_data).items()))

_testing_ids_by_date = copy.deepcopy(_ids_by_dates)
_non_testing_ids_by_date = copy.deepcopy(_ids_by_dates)

for key in _ids_by_dates:
    for id in _ids_by_dates.get(key):
        if int(id) % 2 == 0:
            _testing_ids_by_date.get(key).remove(id)
        else:
            _non_testing_ids_by_date.get(key).remove(id)


_average_testing_likes_by_date = {}
_average_non_testing_likes_by_date = {}

for key in _testing_ids_by_date:
    ids_temp = _testing_ids_by_date.get(key)
    unique = len(set(ids_temp))
    if unique != 0:
        _average_testing_likes_by_date[key] = len(ids_temp) / unique
    else:
        _average_testing_likes_by_date[key] = 0

for key in _non_testing_ids_by_date:
    ids_temp = _non_testing_ids_by_date.get(key)
    unique = len(set(ids_temp))
    if unique != 0:
        _average_non_testing_likes_by_date[key] = len(ids_temp) / unique
    else:
        _average_non_testing_likes_by_date[key] = 0

draw(_average_testing_likes_by_date, _average_non_testing_likes_by_date)

