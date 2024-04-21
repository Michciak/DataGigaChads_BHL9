import streamlit as st
import xai as xai
import plotly.graph_objects as go
import plotly.express as px
from db_handler import *
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

if 'db_b' not in st.session_state:
    st.session_state.db_b = False

if 'new_df' not in st.session_state:
    st.session_state.new_df = None
    st.session_state.new_df_ready = False

# col_db, input_col = st.columns([10,2])
# with input_col:
    st.markdown("""
                    <style>
                    button {
                        height: auto;
                        padding-top: 10px !important;
                        padding-bottom: 10px !important;
                    }</style>""", unsafe_allow_html=True, )
    db_button = st.button('Manage Data', use_container_width=True)
    # if db_button:
    #     st.session_state.db_b = not st.session_state.db_b

# if st.session_state.db_b:
#     with col_db:
st.markdown("# ")

file_up_col, file_push_col = st.columns([6,2])
with file_up_col:
    loaded_csv = st.file_uploader('Wczytaj dane z pliku CSV', type='csv')
    if loaded_csv is not None:
        st.session_state.new_df = pd.read_csv(loaded_csv)
        st.session_state.new_df_ready = True
with file_push_col:
    st.write('')
    st.button('Załaduj dane do bazy', on_click=push_to_db, use_container_width=True, args=(st.session_state.new_df,), disabled=not st.session_state.new_df_ready)
    if st.button('Pobierz dane z bazy', use_container_width=True):
        try:
            st.session_state.data = pull_from_db()
        except Exception as e:
            st.write(str(e))