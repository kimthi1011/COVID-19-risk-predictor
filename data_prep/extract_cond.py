import pandas as pd
import numpy as np

'''
Here, we're trying to take the conditions of patients from positive/negative dataset and apply a date filter using the tested date from positive/negative dataset respectively.
We're doing this cause we say some behavioral disorders in ranked results of ML model. So, we wanted to only consider conditions as listed below -
1. For positive dataset - Consider all the conditions starting 2 weeks prior until the day of initial COVID test.
2. For negative dataset - Consider all the conditions starting 2 weeks prior until their last COVID test.

Note - These COVID tests might be PCR or Antibody tested.
'''

test = pd.read_csv('./parsed_data/tested_negative.csv')
test['MEASUREMENT_DATE'] = pd.to_datetime(test['MEASUREMENT_DATE'])

cond = pd.read_csv('./parsed_data/condition_data_negative.csv')
cond['CONDITION_START_DATE'] = pd.to_datetime(cond['CONDITION_START_DATE'])
test.head()
test.dtypes
cond.head()
cond.dtypes

test = test.sort_values(by=['PERSON_ID','MEASUREMENT_DATE'], ascending=False)   ##True for positive, False for negative to select first/last test respectively.
test['symp_pos'] = test.MEASUREMENT_DATE - pd.to_timedelta(14, unit='d')        ## 14 days prior to the test
test['symp_neg'] = test.MEASUREMENT_DATE - pd.to_timedelta(14, unit='d')        ## 14 days prior to the test
test['symp_pos'] = pd.to_datetime(test['symp_pos'])
test['symp_neg'] = pd.to_datetime(test['symp_neg'])
test = test[test.PERSON_ID.duplicated()==False]
pid = test.PERSON_ID.unique().tolist()
len(test)
#5454 - negative
#614 - positive
test.to_csv('./parsed_data/2week-filter/late_test_negative.csv', index=False)
test.to_csv('./parsed_data/2week-filter/early_test_positive.csv', index=False)

#test = pd.read_csv('./parsed_data/early_test_positive.csv')
test = test.drop(['MEASUREMENT_SOURCE_VALUE', 'VALUE_SOURCE_VALUE'], axis=1).set_index('PERSON_ID')
test.dtypes
test1= test.to_dict('index')
test1[615]

cond=cond[cond.PERSON_ID.isin(pid)]

cond.columns
cond.dtypes
cond1 = pd.DataFrame()
cond.head()
len(cond)


for row in cond.itertuples():
    if(row.CONDITION_START_DATE < test1[row.PERSON_ID]['MEASUREMENT_DATE']):
        cond1 = cond1.append(pd.Series(row),ignore_index=True)
        #row.to_csv('./condition_week.csv', mode='a')



len(cond1)
cond1.tail()
cond1.drop([0],axis=1, inplace=True)
cond1[1] = pd.to_numeric(cond1[1], downcast='integer')
cond1[4] = pd.to_numeric(cond1[4], downcast='integer')
len(cond1)
#2 weeks prior to initial test
#1681 - positive
#26448 - negative

#Any condition to prior test
#77321 - positive
cond1.columns = cond.columns
cond1.dtypes
cond1.sort_values('PERSON_ID').head()
cond1.to_csv('./parsed_data/test_prior_conditions/date-filter-conditions-positive.csv', index=False)
len(cond1.CONDITION_SOURCE_CONCEPT_ID.unique())
#2-week prior conditions to test
#707 - positive
#4373 - negative

#Any prior conditions to test
#6947 - positive