import pandas as pd
import streamlit as st
from io import StringIO
import SessionState
import numpy as np
import plotly.graph_objects as go
import requests
import re
 
st.title("COVID-19 Risk Predictor")
session_state = SessionState.get(score=500, df2 = pd.DataFrame() )

pd.options.display.max_colwidth = 500

@st.cache (hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True) # 👈 This function will be cached
def dataframe():
    df1 = pd.DataFrame()
    df = pd.read_csv('../parsed_data/OMOP.csv')
    #df = df.drop_duplicates()
    #df = pd.read_fwf('./parsed_data/icd10cm_codes_2020.txt', header=None, names=['ICD10','description'],infer_nrows=50000)
    #df = pd.read_fwf("ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2020/icd10cm_codes_2020.txt", header=None, names=['ICD10','description'],infer_nrows=50000)
    df['score'] = np.random.randint(-50,50, size=len(df))
    #df1=pd.read_csv('../parsed_data/person.csv')
    #df=pd.merge(df,df1, on='PERSON_ID',how='outer')
    return df, df1

def imc_chart(imc):
    if (imc>=700):
        color="red"
        '## Alert: Please take a COVID test immediately'
    elif (imc>=550 and imc<700):
        color="orange"
        '## Alert: Please consult a doctor to take COVID test'
    elif (imc>=450 and imc<550):
        color = "lightgreen"
        '## Alert: Please consult a doctor to take COVID test'
    elif (imc<450):
        color="green"
        '## Alert: Please consult a doctor if you have symptoms'
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = imc,
        title = {'text': "Patient Risk Score"},
        delta = {'reference': 500, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [300, 800], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'steps' : [
                {'range': [300, 800], 'color': "white"}],
            'threshold' : {'line': {'color': 'red', 'width': 8}, 
            'thickness': 0.75, 'value': 500}}))

    
    return fig


df, df1= dataframe()
#df
#df.head()

'Number of Conditions in database = ', len(df)
''
''

#gender = st.sidebar.button('Male')
'Gender:'
if st.button('Male'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('Male')])
elif st.button('Female'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('Female')])
elif st.button('Other'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('U')])

'''


'''
'Age range:'
if st.button('<10'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('<10')])
elif st.button('10-30'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('10*30')])
elif st.button('30-50'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('30*50')])
elif st.button('50+'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('50+')])

'''


'''
'Race:'
if st.button('White'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('white')])
elif st.button('African American/Black'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('black')])
elif st.button('Hispanic/Latino'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('latino')])
elif st.button('Other race'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('other race')])

'''


'''
'Smoking History:'
if st.button('Current'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('Current smoker')])
elif st.button('Former'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('former smoker')])
elif st.button('None'):
    session_state.df2= session_state.df2.append(df[df.CONCEPT_NAME.eq('no smoking')])


'''


'''
Test = st.sidebar.text_input("Search condition", 'cough')
if Test:
    df1 = df1.append(df[df.CONCEPT_NAME.str.contains(Test, flags=re.IGNORECASE)])
    Test2 = st.sidebar.multiselect("Select condition", df1['CONCEPT_NAME'].unique())
    if Test2:
         #df1[df1.description.isin(Test2)]
        session_state.df2= session_state.df2.append(df1[df1.CONCEPT_NAME.isin(Test2)])
#    Test3 = st.sidebar.multiselect("Select condition", session_state.df2['description'])
#    if Test3:
#        session_state.df2.drop(session_state.df2[session_state.df2.description.isin(Test3)], inplace=True)

'List of all conditions associated with your search:'
df1
''
''

'List of Patient\'s conditions:'
session_state.df2
'''


'''
if session_state.df2.empty:
    #session_state.score
    st.write(imc_chart(session_state.score))
    '## 💊 Patient Risk Score:', session_state.score 
else:
    session_state.df2 = session_state.df2.drop_duplicates(['CONCEPT_ID'])
    session_state.score = session_state.df2['score'].sum() +500
    st.write(imc_chart(session_state.score))
    '## 💊 Patient Risk Score:', session_state.score 

#st.write(imc_chart(session_state.score))
#'## 💊 Patient Risk Score:', session_state.score 
''
''
#st.image('score.png', caption='Risk score range',
#         use_column_width=True)

