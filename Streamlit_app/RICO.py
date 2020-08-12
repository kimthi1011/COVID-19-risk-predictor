import streamlit as st
import plotly.graph_objects as go

 
st.title("COVID-19 Risk Predictor")
st.markdown("<h3 style='text-align: right;'>by RICO - Team 4</h3>", unsafe_allow_html=True)
''' 
 
 
 
'''
#pd.options.display.max_colwidth = 500

def imc_chart(imc):
    if (imc>=213):
        color="red"
        '## Alert: Please take a COVID test immediately.'
       # '### You are >20% likely.'
    elif (imc>=170 and imc<213):
        color="orange"
        '## Alert: Please consult a doctor to take COVID test'
    elif (imc>=0 and imc<170):
        color = "lightgreen"
        '## Alert: Please consult a doctor to take COVID test'
    elif (imc<0):
        color="green"
        '## Alert: Please consult a doctor if you have symptoms'
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        domain = {'x': [0, 1], 'y': [0, 1]},
        value = imc,
        title = {'text': "Patient Risk Score"},
        delta = {'reference': 213, 'increasing': {'color': "RebeccaPurple"}},
        gauge = {
            'axis': {'range': [-170, 350], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'steps' : [
                {'range': [-170, 350], 'color': "white"}],
            'threshold' : {'line': {'color': 'red', 'width': 8}, 
            'thickness': 0.75, 'value': 213}}))

    
    return fig


age = st.sidebar.selectbox(
     'Please select your age:',
     ('','<20', '20-39','40-54','>55'))

if age =='':
    age = 0
elif age =='<20':
    age = 29
elif age =='20-39':
    age = -15
elif age =='40-54':
    age = 25
elif age =='>55':
    age = -6


race = st.sidebar.selectbox(
     'What was or would be your race on the 2020 census?',
     ('','Decline to answer', 'Asian','White','Black or African American','Hispanic or Latino','Other or Multiple'))
if race =='':
    race = 0
elif race =='Decline to answer':
    race = -34
elif race =='Asian':
    race = 74
elif race =='White':
    race = -27
elif race =='Black or African American':
    race = 26
elif race =='Hispanic or Latino':
    race = 18
elif race =='Other or Multiple':
    race = 35




cough = st.sidebar.selectbox(
     'Do you have a cough?',
     ('','Yes', 'No'))
if cough == '':
    cough = 0
elif cough == 'Yes':
    cough = 79
elif cough == 'No':
    cough = -37

smoke = st.sidebar.selectbox(
     'Do you smoke?',
     ('','Yes', 'No'))
if smoke == '':
    smoke = 0
elif smoke == 'Yes':
    smoke = -64
elif smoke == 'No':
    smoke = 10

drink = st.sidebar.selectbox(
     'Do you drink?',
     ('','Yes', 'No','Former'))
if drink == '':
    drink = 0
elif drink == 'Yes':
    drink = 3
elif drink == 'No':
    drink = 0
elif drink == 'Former':
    drink = -32

fever = st.sidebar.selectbox(
     'Do you have fever?',
     ('','Yes', 'No'))
if fever == '':
    fever = 0
elif fever == 'Yes':
    fever = 33
elif fever == 'No':
    fever = -2

tired = st.sidebar.selectbox(
     'Do you feel tired?',
     ('','Yes', 'No'))
if tired == '':
    tired = 0
elif tired == 'Yes':
    tired = 20
elif tired == 'No':
    tired = -1

muscle = st.sidebar.selectbox(
     'Do you feel muscle pain?',
     ('','Yes', 'No'))
if muscle == '':
    muscle = 0
elif muscle == 'Yes':
    muscle = 25
elif muscle == 'No':
    muscle = -2

mucus = st.sidebar.selectbox(
     'Have you had increased mucus or phlegm?',
     ('','Yes', 'No'))
if mucus == '':
    mucus = 0
elif mucus == 'Yes':
    mucus = 25
elif mucus == 'No':
    mucus = -2

headache = st.sidebar.selectbox(
     'Do you have a headache?',
     ('','Yes', 'No'))
if headache == '':
    headache = 0
elif headache == 'Yes':
    headache = 119
elif headache == 'No':
    headache = -5

t2d = st.sidebar.selectbox(
     'Do you have Type 2 diabetes?',
     ('','Yes', 'No'))
if t2d == '':
    t2d = 0
elif t2d == 'Yes':
    t2d = 12
elif t2d == 'No':
    t2d = -2

pregnant = st.sidebar.selectbox(
     'Are you pregnant?',
     ('','Yes', 'No'))
if pregnant == '':
    pregnant = 0
elif pregnant == 'Yes':
    pregnant = -93
elif pregnant == 'No':
    pregnant = 9

kidney = st.sidebar.selectbox(
     'Are you currently seeing a doctor for kidney issues?',
     ('','Yes', 'No'))
if kidney == '':
    kidney = 0
elif kidney == 'Yes':
    kidney = -85
elif kidney == 'No':
    kidney = 6

hyper = st.sidebar.selectbox(
     'Have you been diagnosed with hypertension?',
     ('','Yes', 'No'))
if hyper == '':
    hyper = 0
elif hyper == 'Yes':
    hyper = -40
elif hyper == 'No':
    hyper = 8

heart = st.sidebar.selectbox(
     'Have you been diagnosed with heart disease (other than hypertension)?',
     ('','Yes', 'No'))
if heart == '':
    heart = 0
elif heart == 'Yes':
    heart = -56
elif heart == 'No':
    heart = 4


anxiety = st.sidebar.selectbox(
     'Have you been diagnosed with an anxiety disorder?',
     ('','Yes', 'No'))
if anxiety == '':
    anxiety = 0
elif anxiety == 'Yes':
    anxiety = -64
elif anxiety == 'No':
    anxiety = 4

copd = st.sidebar.selectbox(
     'Have you been diagnosed with COPD?',
     ('','Yes', 'No'))
if copd == '':
    copd = 0
elif copd == 'Yes':
    copd = -101
elif copd == 'No':
    copd = 3

 
total = 137 + cough + smoke + fever + tired +muscle + mucus +headache +t2d + pregnant + kidney + heart + anxiety + hyper + copd + drink + age + race
st.write(imc_chart(total))
'## 💊 Patient Risk Score:', total 

'''
---

Risk score chart:
------------------
####    Base score = 137
 

Predictive safest score < 0

Predictive safe score = 0 - 170

Predictive risk score = 170 - 213

Predictive high risk = >213

'''