import streamlit as st
import xai as xai
import plotly.graph_objects as go
import plotly.express as px
from db_handler import *
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class YearFromDtTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Assuming X is a DataFrame and "Dt_Customer" is one of its columns
        year_column = X["Dt_Customer"].str[:4].astype(int)
        return year_column.values.reshape(-1, 1)

exp = xai.build_exp()

categories = [
        'Education',
        'Marital_Status',
        'KidHome',
        'TeenHome',
        'AcceptedCmp1',
        'AcceptedCmp2',
        'AcceptedCmp3',
        'AcceptedCmp4',
        'AcceptedCmp5'
    ]

if 'data' not in st.session_state:
    st.session_state.data = pd.read_csv("marketing_campaign.csv", sep = ";")

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

st.title("Informacje o wykorzystywanym modelu")

st.write(st.session_state.mp)