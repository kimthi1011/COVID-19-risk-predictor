import pandas as pd


test1=pd.read_csv('./parsed_data/condition_data_positive.csv')
test1.columns
test1 = test1[['PERSON_ID','CONDITION_SOURCE_CONCEPT_ID']]
test1.head()
test1 = test1.drop_duplicates()
len(test1)

df = pd.get_dummies(test1, columns=['CONDITION_SOURCE_CONCEPT_ID'])
df.shape
df.head(3)