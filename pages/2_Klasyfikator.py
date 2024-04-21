import streamlit as st
import xai as xai
import pickle as pkl
import plotly.graph_objects as go
import plotly.express as px
from db_handler import *
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

# if 'data' not in st.session_state:
#     st.session_state.data = pd.read_csv("marketing_campaign.csv", sep = ";")

st.set_page_config(page_title="Sentiment Analysis", layout="wide")

class YearFromDtTransformer(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        # Assuming X is a DataFrame and "Dt_Customer" is one of its columns
        year_column = X["Dt_Customer"].str[:4].astype(int)
        return year_column.values.reshape(-1, 1)
    
class RemoveDumbYearBirth(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.median_year_birth = X["Year_Birth"].median().astype(int)
        return self
    
    def transform(self, X):
        X.loc[X["Year_Birth"]<1930, "Year_Birth"] = self.median_year_birth
        return X["Year_Birth"].values.reshape(-1, 1)
    
class RemoveDumbIncome(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def fit(self, X, y=None):
        self.median_income = X["Income"].median().astype(int)
        return self
    
    def transform(self, X):
        X.loc[X["Income"]>200000, "Income"] = self.median_income
        return X["Income"].values.reshape(-1, 1)

st.title("Wykorzystywany model")

if 'model_name' not in st.session_state:
    st.session_state.model_name = ''

st.session_state.model_name = st.selectbox("Model klasyfikatora", ["XGBoost", "Regresja liniowa"])
if st.session_state.model_name == 'XGBoost':
    with st.spinner('Inicjalizowanie klasyfikatora...'):
        st.session_state.exp = xai.build_exp("models/xgb.pkl")
        st.session_state.mp = xai.vip(st.session_state.exp)
        exclude_values = ["_baseline_", "_full_model_", "ID", "Z_Revenue"]
        st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')

elif st.session_state.model_name == 'Regresja liniowa':
    with st.spinner('Inicjalizowanie klasyfikatora...'):
        st.session_state.exp = xai.build_exp("models/lr.pkl")
        st.session_state.mp = xai.vip(st.session_state.exp)
        exclude_values = ["_baseline_", "_full_model_", "ID", "Z_Revenue"]
        st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')


st.write(st.session_state.mp)