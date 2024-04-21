import streamlit as st
import xai as xai
import plotly.graph_objects as go
import plotly.express as px
from db_handler import *
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

with st.spinner("Inicjalizowanie aplikacji..."):

    # if 'mp' not in st.session_state:
    #     st.session_state.exp = xai.build_exp("models/xgb.pkl")
    #     st.session_state.mp = xai.vip(st.session_state.exp)
    #     exclude_values = ["_baseline_","_full_model_","ID","Z_Revenue"]
    #     st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')

    # if 'mp' not in st.session_state:
    #     st.session_state.mp = xai.vip(exp)
    #     exclude_values = ["_baseline_","_full_model_","ID","Z_Revenue"]
    #     st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')

    if 'new_df' not in st.session_state:
        st.session_state.new_df = None
        st.session_state.new_df_ready = False

    if 'data' not in st.session_state:
        try:
            st.session_state.data = pull_from_db()
        except:
            st.session_state.data = pd.read_csv("marketing_campaign.csv", sep = ";")