import pandas as pd

'''
Map all the conditions of patients to OMOP database.
We're trying to map to ICD10 codes for easy filtering and converting to categorical values.

'''

pos=pd.read_csv('./parsed_data/2week-filter/date-filter-conditions-positive.csv')
pos.head()

'''
#Use this code to only extract the ICD10 code from the whole database with other codes.

omop = pd.read_csv('./parsed_data/OMOP_CONCEPT.txt', sep="|")
omop.head(5)
omop = omop[['CONCEPT_ID','CONCEPT_NAME','VOCABULARY_ID','CONCEPT_CODE']]
omop = omop[omop['VOCABULARY_ID']=='ICD10CM']
omop1 = omop.drop(omop.loc[omop['CONCEPT_CODE']=='U07.1'].index)
omop1.to_csv('./parsed_data/OMOP.csv', index=False)
'''

omop1 = pd.read_csv('./parsed_data/OMOP.csv')
len(omop1)
#96307 ICD10 codes

merge = pd.merge(pos,omop1,left_on='CONDITION_SOURCE_CONCEPT_ID',right_on='CONCEPT_ID', how='left')
merge.head()
#merge.to_csv('./parsed_data/ID-merged-condition-negative.csv',index=False)

#check for specific concept ID
#upos = merge[merge['CONCEPT_CODE']=='U07.1']
upos = merge[~merge['CONCEPT_CODE'].isna()]
len(upos['PERSON_ID'].unique())
#2260 negative patients
#242 positive patients


upos.head()
upos['group'] = upos['CONCEPT_CODE'].astype(str).str[0]
upos = upos[['PERSON_ID','CONCEPT_CODE', 'group']]
upos.to_csv('./parsed_data/2week-filter/date-filter-ICD10_grouped_positive.csv', index=False)

#merge[merge['CONCEPT_CODE'].isna()].to_csv('./parsed_data/unmap_conditions_positive.csv', index=False)