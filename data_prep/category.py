import pandas as pd


test1=pd.read_csv('./parsed_data/2week-filter/date-filter-ICD10_grouped_negative.csv').set_index('PERSON_ID')
test1.head()
test1.drop('CONCEPT_CODE', axis=1, inplace = True)
test = pd.get_dummies(test1).groupby(level=0).sum()
test.head()
test.to_csv('./parsed_data/2week-filter/sum-catc-negative.csv')