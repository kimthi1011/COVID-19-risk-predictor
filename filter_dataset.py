import pandas as pd
import re


'''
Extract features like age, sex, race, ethnicity and vital status (live/dead).

Use the below code by changing the file name for positive and negative tested dataset.
'''

#open and read person.csv file
test3 = pd.read_csv('../UAB_LDS/Cohort3/2020-JUNE-hackathon-N3C-covid19-Negative/person.csv', sep="|", header = 0)
test3 = test3[['PERSON_ID','YEAR_OF_BIRTH','GENDER_SOURCE_VALUE','RACE_SOURCE_VALUE','ETHNICITY_SOURCE_VALUE']]
test3['approx_age'] = 2020-test3['YEAR_OF_BIRTH']
len(test3.index.unique())
test3.head(10)
pid = test3.PERSON_ID.unique().tolist()
#test3=test3[test3.PERSON_ID.isin(pid)]
#test3.drop('YEAR_OF_BIRTH',inplace=True, axis=1)
test3.columns


#open and read death.csv file
test4 = pd.read_csv('../UAB_LDS/Cohort3/2020-JUNE-hackathon-N3C-covid19-Negative/death.csv', sep="|", header = 0)
test4 = test4[['PERSON_ID','DEATH_DATE']]
test4=test4[test4.PERSON_ID.isin(pid)]
test4 = pd.merge(test3,test4, on='PERSON_ID', how='outer')
len(test4.index)
test4.columns
test4.to_csv('./parsed_data/person_negative.csv',index=False)



'''
open and read measurement.csv file for both positive and negative tested dataset.
We try to extract COVID tests and results along with dates of patients.
'''
#Find number of patients from positive/negative dataset who got tested to extract the measurements of only those patients.
test1=pd.read_csv('./parsed_data/person_positive.csv')
test1 = test1.sort_values(by='PERSON_ID')
test1.head()
pid = test1.PERSON_ID.unique().tolist()
#len(pid)

#Read the file measurement.csv and extract the tests and results
test = pd.read_csv('../UAB_LDS/Cohort1/2020-JUNE-hackathon-N3C-covid19-Positive/measurement.csv', sep="|", header = 0)
test.head()
test = test[['PERSON_ID','MEASUREMENT_DATE','MEASUREMENT_SOURCE_VALUE','VALUE_SOURCE_VALUE']]
test=test[test.PERSON_ID.isin(pid)]
len(test['MEASUREMENT_SOURCE_VALUE'])
test = test[test.MEASUREMENT_SOURCE_VALUE.str.contains('cov',regex=True,na=False, flags = re.IGNORECASE) & ~test.MEASUREMENT_SOURCE_VALUE.str.contains('quest',regex=True,na=False, flags = re.IGNORECASE)]
pid = test.PERSON_ID.unique().tolist()
test['MEASUREMENT_DATE'] = pd.to_datetime(test['MEASUREMENT_DATE'])
test.to_csv('./parsed_data/tested.csv', index=False)


'''
This is the main file that we want to work on. condition_occurance.csv has a list of "all" conditions a patient has or been reported in EHR. 
Since the concepts in this file are corrupted, we try to use concept IDs and map them to ICD10 codes available at OMOP database (file will be used in map.py to actually map)
Here, we're trying to extract ID, condition date, condition itself and concept ID annotated to it.
'''

#open and read condition_occurrence.csv file
test1 = pd.read_csv('../UAB_LDS/Cohort1/2020-JUNE-hackathon-N3C-covid19-Positive/condition_occurrence.csv', sep="|", header = 0)
test1 = test1[['PERSON_ID','CONDITION_START_DATE','CONDITION_SOURCE_VALUE','CONDITION_SOURCE_CONCEPT_ID']]
#len(test1.CONDITION_SOURCE_CONCEPT_ID.unique())
#len(test1.CONDITION_SOURCE_VALUE.unique())
#test1[test1['CONDITION_SOURCE_VALUE'].isnull()]
test1=test1[test1.PERSON_ID.isin(pid)]
test1.columns
test1.to_csv('./parsed_data/condition_data_positive.csv',index=False)

#Extract and count number of conditions
df = test1.drop(['PERSON_ID','CONDITION_START_DATE','CONDITION_SOURCE_VALUE'], axis=1)
df.head()
len(df)
df = df.drop_duplicates()
#test1['CONDITION_START_DATE'] = pd.to_datetime(test1['CONDITION_START_DATE'])
#test1.dtypes

#df.to_csv('./parsed_data/concepts.csv', index=False)
#print(test.head(5))


'''
observation.csv is the file to find things like smoking, alcohol, drug abuse and even diet, exercise and BMI.
Use the same code for both positive and negative tested dataset.
'''

#open and read observation.csv file
test2 = pd.read_csv('../UAB_LDS/Cohort3/2020-JUNE-hackathon-N3C-covid19-Negative/observation.csv', sep="|", header = 0)
test2 = test2[['PERSON_ID','OBSERVATION_DATE','VALUE_AS_STRING','OBSERVATION_SOURCE_VALUE','QUALIFIER_SOURCE_VALUE']]
len(test2.index)
test2=test2[test2.PERSON_ID.isin(pid)]
#test2 = pd.read_csv('./parsed_data/observation_Negative.csv')
test2['OBSERVATION_DATE'] = pd.to_datetime(test2['OBSERVATION_DATE'])
#test1.dtypes

test2.dtypes
test2.head(50)

#Extract only the below features of patients
options = ['SHX Alcohol use','SHX Substance abuse use','SHX Tobacco use']
test2 = test2[test2['OBSERVATION_SOURCE_VALUE'].isin(options) | test2['OBSERVATION_SOURCE_VALUE'].str.contains('Z68')].sort_values(by=['PERSON_ID','OBSERVATION_DATE','QUALIFIER_SOURCE_VALUE'])
test = test2.groupby(['PERSON_ID', 'QUALIFIER_SOURCE_VALUE'], as_index=False).last()
test = test.drop(['QUALIFIER_SOURCE_VALUE','OBSERVATION_DATE'], axis=1)
test.to_csv('./parsed_data/observation_Negative.csv',index=False)

