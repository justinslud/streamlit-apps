import streamlit as st
import numpy as np
import pandas as pd
import requests
import pickle

import matplotlib.pyplot as plt
import bokeh
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer

subject_model = pickle.load(open('models/subject_model.p', 'rb'))

headlines = pd.read_csv('data/1995-2017clean.csv')

top_subjects = ['armed conflicts', 'art and culture', 'business', 'disasters', 'international relations', 'law', 'politics', 'science', 'sports']

default_headline = 'Usain bolt wins the 100 meter dash in the London 2012 Olympics.'

default_keyword = 'Tom Brady'

@st.cache
def predict_subject(headline):
    return {'subject': str(subject_model.predict([headline])[0]),
            'all_proba': dict(zip(top_subjects, list(subject_model.predict_proba([headline])[0])))
            }

@st.cache
def keyword_counts(keyword):
    matches = headlines[(headlines.text.str.contains(keyword)) | (headlines.event.str.contains(keyword))].drop('day', axis=1)
    counts = matches.groupby('year').text.count()
    return counts

def trend_plot(keyword):
    counts = keyword_counts(keyword)
    cds = ColumnDataSource(pd.DataFrame(data=counts))
    p = figure(plot_width = 400, plot_height = 400, tools='hover', tooltips='@text', title = 'Wikipedia Current News mentions for {}'.format(keyword))
    p.line(counts.index, counts.values)

    p.circle('year', 'text', size=5, fill_color='grey', fill_alpha=.4, \
             hover_color='lightblue', hover_alpha=.2, source=cds)

    return p
                                        

def run_wcea():

    task = st.sidebar.selectbox('Pick a task', ['Predict Subject', 'Trend Plot'])

    st.markdown('## ' + task)

    if task == 'Predict Subject':

        possible_subjects = st.markdown('Possible subjects: ' + ', '.join(top_subjects))

        headline = st.text_input('Your headline', default_headline)

        response = predict_subject(headline)

        subject = response['subject']

        st.markdown('Predicted Subject: **{}**'.format(subject))

        proba = pd.Series(response['all_proba'])
        
        st.bar_chart(proba.sort_values(ascending=False))


    elif task == 'Trend Plot':

        keyword = st.text_input('Your keyword', default_keyword)

        st.bokeh_chart(trend_plot(keyword))
