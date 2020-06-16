import pandas as pd

test = pd.read_csv('./parsed_data/tested.csv')
test['MEASUREMENT_DATE'] = pd.to_datetime(test['MEASUREMENT_DATE'])

cond = pd.read_csv('./parsed_data/condition_data.csv')
cond['CONDITION_START_DATE'] = pd.to_datetime(cond['CONDITION_START_DATE'])
test.head()
test.dtypes
cond.head()
cond.dtypes

test = test.sort_values(by=['PERSON_ID','MEASUREMENT_DATE'], ascending=True)
test['symp_onset'] = test.MEASUREMENT_DATE - pd.to_timedelta(14, unit='d')
test['symp+7'] = test.MEASUREMENT_DATE + pd.to_timedelta(14, unit='d')
test = test[test.PERSON_ID.duplicated()==False]
len(test)
test.to_csv('./parsed_data/early_test.csv', index=False)

test = test.drop(['MEASUREMENT_SOURCE_VALUE', 'VALUE_SOURCE_VALUE','MEASUREMENT_DATE'], axis=1).set_index('PERSON_ID')
test1= test.to_dict('index')
test1[2]

cond.columns
cond1 = pd.DataFrame()
cond.head()

for row in cond.itertuples():
    if ((row.CONDITION_START_DATE < test1[row.PERSON_ID]['symp+7']) & (row.CONDITION_START_DATE > test1[row.PERSON_ID]['symp_onset'])):
        cond1 = cond1.append(pd.Series(row),ignore_index=True)
        #row.to_csv('./condition_week.csv', mode='a')

cond1.drop([0],axis=1, inplace=True)
cond1[1] = pd.to_numeric(cond1[1], downcast='integer')
cond1[4] = pd.to_numeric(cond1[4], downcast='integer')
cond1.columns = cond.columns
cond1.dtypes
cond1.head()
cond1.to_csv('./parsed_data/date-filter-conditions.csv', index=False)
len(cond1.CONDITION_SOURCE_CONCEPT_ID.unique())