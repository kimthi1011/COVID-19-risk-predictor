import pandas as pd
import streamlit as st
from io import StringIO
import SessionState
import numpy as np
import plotly.graph_objects as go
import requests
import re

st.title("COVID-19 Risk Predictor")
session_state = SessionState.get(df2 = pd.DataFrame())
pd.options.display.max_colwidth = 500

@st.cache (hash_funcs={StringIO: StringIO.getvalue}, suppress_st_warning=True) # 👈 This function will be cached
def dataframe():
    df1 = pd.DataFrame()
    df = pd.read_csv('../parsed_data/concepts.csv',names=['description','ID'])
    df = df.drop_duplicates()
    #df = pd.read_fwf('./parsed_data/icd10cm_codes_2020.txt', header=None, names=['ICD10','description'],infer_nrows=50000)
    #df = pd.read_fwf("ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Publications/ICD10CM/2020/icd10cm_codes_2020.txt", header=None, names=['ICD10','description'],infer_nrows=50000)
    df['score'] = np.random.randint(-10,10, size=len(df))
    #df1=pd.read_csv('../parsed_data/person.csv')
    #df=pd.merge(df,df1, on='PERSON_ID',how='outer')
    return df, df1

def imc_chart(imc):
    if (imc>=7):
        color="red"
    elif (imc>=5 and imc<7):
        color="orange"
    elif (imc>=3 and imc<5):
        color = "lightgreen"
    elif (imc<3):
        color="green"
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = imc,
        title = {'text': "Patient Risk Score"},
        delta = {'reference': 5, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [0, 10], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'steps' : [
                {'range': [0, 10], 'color': "white"}],
            'threshold' : {'line': {'color': 'red', 'width': 8}, 
            'thickness': 0.75, 'value': 5}}))

    
    return fig


df, df1= dataframe()
#df

'Number of Conditions in database = ', len(df)
''
''
Test = st.sidebar.text_input("Search condition", 'cough')
if Test:
    df1 = df1.append(df[df.description.str.contains(Test, flags=re.IGNORECASE)])
    Test2 = st.sidebar.multiselect("Select condition", df1['ID'].unique())
    if Test2:
         #df1[df1.description.isin(Test2)]
        session_state.df2= session_state.df2.append(df1[df1.ID.isin(Test2)])
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
score = session_state.df2['score'].sum()
st.write(imc_chart(score))
'## 💊 Patient Risk Score:', score 
''
''
#st.image('score.png', caption='Risk score range',
#         use_column_width=True)

