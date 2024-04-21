import streamlit as st
import xai as xai
import plotly.graph_objects as go
import plotly.express as px
from db_handler import *
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

st.markdown("""W twoich dłoniach znalazło się potężne narzędzie. Pozwoli ci ono przewidzieć skuteczność twojej następnej kampanii marketingowej oraz zrozumieć co miało największy wpływ na wyniki twojej poprzedniej kampanii. 
            Pamiętaj proszę, że to narzędzie ma cię wesprzeć w podejmowaniu decyzji, a nie zastąpić.""")

with st.spinner("Inicjalizowanie aplikacji..."):
    pass
    # if 'mp' not in st.session_state:
    #     st.session_state.exp = xai.build_exp("models/xgb.pkl")
    #     st.session_state.mp = xai.vip(st.session_state.exp)
    #     exclude_values = ["_baseline_","_full_model_","ID","Z_Revenue"]
    #     st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')

    # if 'mp' not in st.session_state:
    #     st.session_state.mp = xai.vip(exp)
    #     exclude_values = ["_baseline_","_full_model_","ID","Z_Revenue"]
    #     st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')

