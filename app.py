import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import base64
#import matplotlib.pyplot as plt

st.title("COVID-19 condition data")

@st.cache  # 👈 This function will be cached
def dataframe():
    df = pd.read_csv('../parsed_data/tested.csv')
    df1=pd.read_csv('../parsed_data/person.csv')
    df=pd.merge(df,df1, on='PERSON_ID',how='outer')
    return df

df=dataframe()
if st.checkbox('Show Data'):
   df

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="filtered.csv">Download filtered csv</a>'



age = st.sidebar.slider(
    'Select age range',
    min(df.approx_age),max(df.approx_age), (25, 50))
    

Test = st.sidebar.multiselect("COVID-19 Tests", df['MEASUREMENT_SOURCE_VALUE'].unique())
if Test:
    df = df[df.MEASUREMENT_SOURCE_VALUE.isin(Test)]
    

Test2 = st.sidebar.multiselect("COVID-19 Test Result", df['VALUE_SOURCE_VALUE'].unique())
if Test2:
    df = df[df.VALUE_SOURCE_VALUE.isin(Test2)]

Test3 = st.sidebar.multiselect("Gender", df['GENDER_SOURCE_VALUE'].unique())
if Test3:
    df = df[df.GENDER_SOURCE_VALUE.isin(Test3)]

Test4 = st.sidebar.multiselect("Race", df['RACE_SOURCE_VALUE'].unique())
if Test4:
    df = df[df.RACE_SOURCE_VALUE.isin(Test4)]
    
df = df[(df.approx_age >= age[0]) & (df.approx_age <= age[1])]
df
"Number of patients = " , len(df['PERSON_ID'].unique())

#if st.button('Download Filtered data'):
st.markdown(get_table_download_link(df), unsafe_allow_html=True)














