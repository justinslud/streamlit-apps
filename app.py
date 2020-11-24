import streamlit as st

from wikipedia_current_events_analysis import run_wcea

projects = ['Wikipedia Current News Analysis', 'Second Project']

title = st.empty()

st.markdown('by [Justin Slud](https://justinslud.github.io/about-contact)')

project = st.sidebar.selectbox('Choose a project to get started', projects)

title.title(project)

if option == 'Wikipedia Current News Analysis':
    run_wcea()


elif option == 'Second Project':
    pass

