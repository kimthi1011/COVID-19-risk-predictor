import pandas as pd
import re

#open and read measurement.csv file
test = pd.read_csv('../UAB_LDS/Cohort1/2020-JUNE-hackathon-N3C-covid19-Positive/measurement.csv', sep="|", header = 0)
test.head()
test = test[['PERSON_ID','MEASUREMENT_DATE','MEASUREMENT_SOURCE_VALUE','VALUE_SOURCE_VALUE']]
test = test[test.MEASUREMENT_SOURCE_VALUE.str.contains('cov',regex=True,na=False, flags = re.IGNORECASE) & ~test.MEASUREMENT_SOURCE_VALUE.str.contains('quest',regex=True,na=False, flags = re.IGNORECASE)]
pid = test.PERSON_ID.unique().tolist()
test['MEASUREMENT_DATE'] = pd.to_datetime(test['MEASUREMENT_DATE'])
test.to_csv('./parsed_data/tested.csv', index=False)

#Find number of patients who got tested
#test=pd.read_csv('./parsed_data/tested.csv')
#pid = test.PERSON_ID.unique().tolist()
#len(pid)


#open and read condition_occurrence.csv file
test1 = pd.read_csv('condition_occurrence.csv', sep="|", header = 0)
test1 = test1[['PERSON_ID','CONDITION_START_DATE','CONDITION_SOURCE_VALUE','CONDITION_SOURCE_CONCEPT_ID']]
#len(test1.CONDITION_SOURCE_CONCEPT_ID.unique())
#len(test1.CONDITION_SOURCE_VALUE.unique())
#test1[test1['CONDITION_SOURCE_VALUE'].isnull()]
test1=test1[test1.PERSON_ID.isin(pid)]
df = test1.drop(['PERSON_ID','CONDITION_START_DATE'], axis=1)
len(df)
df = df.drop_duplicates()
#test1['CONDITION_START_DATE'] = pd.to_datetime(test1['CONDITION_START_DATE'])
#test1.dtypes
test1.to_csv('./parsed_data/condition_data.csv',index=False)
df.to_csv('./parsed_data/concepts.csv', index=False)
#print(test.head(5))


#open and read observation.csv file
test2 = pd.read_csv('observation.csv', sep="|", header = 0)
test2 = test2[['PERSON_ID','OBSERVATION_DATE','VALUE_AS_STRING','OBSERVATION_SOURCE_VALUE','QUALIFIER_SOURCE_VALUE']]
len(test2.index)
test2=test2[test2.PERSON_ID.isin(pid)]
test2['OBSERVATION_DATE'] = pd.to_datetime(test2['OBSERVATION_DATE'])
#test1.dtypes
test2.to_csv('./parsed_data/observation.csv',index=False)


#open and read person.csv file
test3 = pd.read_csv('person.csv', sep="|", header = 0)
test3 = test3[['PERSON_ID','YEAR_OF_BIRTH','GENDER_SOURCE_VALUE','RACE_SOURCE_VALUE','ETHNICITY_SOURCE_VALUE']]
test3['approx_age'] = 2020-test3['YEAR_OF_BIRTH']
len(test3.index)
test3=test3[test3.PERSON_ID.isin(pid)]
test3.drop('YEAR_OF_BIRTH',inplace=True, axis=1)
test3.columns

#open and read death.csv file
test4 = pd.read_csv('death.csv', sep="|", header = 0)
test4 = test4[['PERSON_ID','DEATH_DATE']]
test4=test4[test4.PERSON_ID.isin(pid)]
test4 = pd.merge(test3,test4, on='PERSON_ID', how='outer')
len(test4.index)
test4.columns
test4.to_csv('./parsed_data/person.csv',index=False)