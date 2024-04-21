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

st.set_page_config(page_title="Profiler klientów", layout="wide")

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

if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = "Wybierz model"

    if 'new_df' not in st.session_state:
        st.session_state.new_df = None
        st.session_state.new_df_ready = False
        st.session_state.fit_ready = False

    if 'data' not in st.session_state:
        try:
            st.session_state.data = pull_from_db()
        except:
            st.session_state.data = pd.read_csv("marketing_campaign.csv", sep = ";")

st.session_state.model_name = st.selectbox("Model klasyfikatora", ("XGBoost", "Regresja logistyczna"), index=None, placeholder = st.session_state.model_loaded)
if st.session_state.model_name == 'XGBoost':
    if st.session_state.model_loaded != st.session_state.model_name:
        with st.spinner('Inicjalizowanie klasyfikatora...'):
            st.session_state.exp = xai.build_exp("models/xgb.pkl")
            st.session_state.mp = xai.vip(st.session_state.exp)
            exclude_values = ["_baseline_", "_full_model_", "ID", "Z_Revenue"]
            st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')
            st.session_state.pdp = xai.pdp(st.session_state.exp, list(st.session_state.mp["variable"]))
            st.session_state.pdp_cat = xai.pdp_cat(st.session_state.exp, list(st.session_state.mp["variable"]))
            st.session_state.model_loaded = st.session_state.model_name

elif st.session_state.model_name == 'Regresja logistyczna':
    if st.session_state.model_loaded != st.session_state.model_name:
        with st.spinner('Inicjalizowanie klasyfikatora...'):
            st.session_state.exp = xai.build_exp("models/lr.pkl")
            st.session_state.mp = xai.vip(st.session_state.exp)
            exclude_values = ["_baseline_", "_full_model_", "ID", "Z_Revenue"]
            st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')
            st.session_state.pdp = xai.pdp(st.session_state.exp, list(st.session_state.mp["variable"]))
            st.session_state.pdp_cat = xai.pdp_cat(st.session_state.exp, list(st.session_state.mp["variable"]))
            st.session_state.model_loaded = st.session_state.model_name


st.divider()
st.markdown("# Przeszkalanie klasyfikatora")

file_up_col, file_push_col = st.columns([6,2])
with file_up_col:
    loaded_csv = st.file_uploader('Wczytaj dane z pliku CSV', type='csv')
    if loaded_csv is not None:
        st.session_state.new_df = pd.read_csv(loaded_csv, sep = ";")
        st.session_state.new_df_ready = True
        if st.session_state.model_loaded != "Wybierz model":
            st.session_state.fit_ready = True
with file_push_col:
    st.write('')
    if st.button('Załaduj dane do bazy', use_container_width=True, disabled=not st.session_state.new_df_ready):
        try:
            push_to_db(st.session_state.new_df)
        except Exception as e:
            st.write(str(e))
    if st.button('Pobierz dane z bazy', use_container_width=True):
        try:
            st.session_state.data = pull_from_db()
            if st.session_state.model_loaded != "Wybierz model":
                st.session_state.fit_ready = True
        except Exception as e:
            st.write(str(e))


if st.session_state.new_df_ready:
    from_csv = st.checkbox("Użyj danych z pliku CSV", True)

if st.button('Przeucz model przy użyciu nowych danych', disabled=not st.session_state.fit_ready):
    try:
        if from_csv:
            dane = st.session_state.new_df
        elif st.session_state.data is not None:
            dane = st.session_state.data
        else:
            raise Exception('Brak danych do przeuczania modelu')
        with st.spinner('Przeuczanie modelu przy użyciu nowych danych'):
            if st.session_state.model_loaded == 'XGBoost':
                st.session_state.exp = xai.build_exp("models/xgb.pkl")
            if st.session_state.model_loaded == 'Regresja logistyczna':
                st.session_state.exp = xai.build_exp("models/lr.pkl")
            st.session_state.mp = xai.vip(st.session_state.exp)
            exclude_values = ["_baseline_", "_full_model_", "ID", "Z_Revenue"]
            st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')
            st.session_state.pdp = xai.pdp(st.session_state.exp, list(st.session_state.mp["variable"]))
            st.session_state.pdp_cat = xai.pdp_cat(st.session_state.exp, list(st.session_state.mp["variable"]))
    except Exception as e:
        st.write(str(e))




