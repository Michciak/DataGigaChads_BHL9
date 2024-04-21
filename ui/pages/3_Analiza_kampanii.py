import streamlit as st
import xai as xai
import plotly.graph_objects as go
import plotly.express as px
from db_handler import *
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import train_test_split
import pandas as pd

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
#

if 'pdp_cat' not in st.session_state:
    st.markdown("## Najpierw wybierz model w zakładce `Ustawienia`")
else:
    categories = [
            'Education',
            'Marital_Status',
            'KidHome',
            'TeenHome',
            'AcceptedCmp1',
            'AcceptedCmp2',
            'AcceptedCmp3',
            'AcceptedCmp4',
            'AcceptedCmp5',
            'Dt_Customer'
        ]

    # if 'data' not in st.session_state:
    #     try:
    #         st.session_state.data = pull_from_db()
    #     except:
    #         st.session_state.data = pd.read_csv("marketing_campaign.csv", sep = ";")

    st.markdown("""
    <style>
    .big-font {
        font-size:62px !important;
        font-weight: bold;
        line-height: 0.45;
    }
    </style>
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:2rem;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 48px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 100px;
    }
    [data-testid="stMetricDelta"] {
        font-size: 26px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("Analiza kampanii marketingowej")
    st.header("W oparciu o profilowanie klienta")

    # with st.sidebar:
    #     st.header("XD")

    c1,c2,c3,c4,c5 = st.columns(5)
    try:
        with st.spinner("Profilowanie klientów..."):
            with c1:
                st.metric(f"#### Sukces kampanii nr 1", f"{round(st.session_state.data['AcceptedCmp1'].sum()/len(st.session_state.data)*100,2)}%")
            with c2:
                st.metric("#### Sukces kampanii nr 2", f"{round(st.session_state.data['AcceptedCmp2'].sum()/len(st.session_state.data)*100,2)}%", delta=f"{round(round(st.session_state.data['AcceptedCmp2'].sum()/len(st.session_state.data)*100,2)-round(st.session_state.data['AcceptedCmp1'].sum()/len(st.session_state.data)*100,2),2)}%")
            with c3:
                st.metric("#### Sukces kampanii nr 3", f"{round(st.session_state.data['AcceptedCmp3'].sum()/len(st.session_state.data)*100,2)}%", delta=f"{round(round(st.session_state.data['AcceptedCmp3'].sum()/len(st.session_state.data)*100,2)-round(st.session_state.data['AcceptedCmp2'].sum()/len(st.session_state.data)*100,2),2)}%")
            with c4:
                st.metric("#### Sukces kampanii nr 4", f"{round(st.session_state.data['AcceptedCmp4'].sum()/len(st.session_state.data)*100,2)}%", delta=f"{round(round(st.session_state.data['AcceptedCmp4'].sum()/len(st.session_state.data)*100,2)-round(st.session_state.data['AcceptedCmp3'].sum()/len(st.session_state.data)*100,2),2)}%")
            with c5:
                st.metric("#### Sukces kampanii nr 5", f"{round(st.session_state.data['AcceptedCmp5'].sum()/len(st.session_state.data)*100,2)}%", delta=f"{round(round(st.session_state.data['AcceptedCmp5'].sum()/len(st.session_state.data)*100,2)-round(st.session_state.data['AcceptedCmp4'].sum()/len(st.session_state.data)*100,2),2)}%")
    except:
        pass

    st.divider()

    c1,c2,c3,c4,c5 = st.columns(5)
    try:
        Target = 'Response'
        Predictors = [col for col in st.session_state.data.columns.to_list() if col != Target]
        x_train, x_test, y_train, y_test = train_test_split(st.session_state.data[Predictors], st.session_state.data[Target])
        with c2:
            st.metric("#### Sukces poprzedniej kamapnii", f"{round(y_train.sum()/len(y_train)*100,2)}%")
        with c4:
            st.metric("#### Prognozowany sukces kamapnii", f"{round(xai.exp_pred(st.session_state.exp, x_test).sum()/len(x_test)*100,2)}%", delta=f"{round(xai.exp_pred(st.session_state.exp, x_test).sum()/len(x_test)*100,2)-round(y_train.sum()/len(y_train)*100,2)}%")
    except:
        pass

    st.divider()

    st.title("Analiza profilu klienta")

    st.write("Wybierz jaką liczbę cech chcesz uwzględnić:")
    vips = st.slider("Liczba cech klienta",1,10,value=5)

    st.header("Najbardziej wpływowe cechy")
    st.subheader("Na podstawie modelu AI")
    if 'mp' not in st.session_state:
        st.session_state.mp = xai.vip(exp)
        exclude_values = ["_baseline_","_full_model_","ID","Z_Revenue"]
        st.session_state.mp = st.session_state.mp.query('variable not in @exclude_values')

    mp = st.session_state.mp.sort_values(by="dropout_loss", ascending=False).head(n=vips)

    desc_dict = {
    'AcceptedCmp1':  'czy klient zaakceptował ofertę 1 kampanii',
    'AcceptedCmp2':  'czy klient zaakceptował ofertę 2 kampanii',
    'AcceptedCmp3':  'czy klient zaakceptował ofertę 3 kampanii',
    'AcceptedCmp4':  'czy klient zaakceptował ofertę 4 kampanii',
    'AcceptedCmp5':  'czy klient zaakceptował ofertę 5 kampanii',
    'Response': 'czy klient zaakceptował ofertę ostatniej kampanii',
    'Complain': 'czy klient składał skargę w przeciągu dwóch ostanich lat',
    'Dt_Customer': 'data założenia konta',
    'Education': 'poziom edukacji klienta',
    'Marital_Status': 'stan cywilny klienta',
    'Kidhome': 'liczba małych dzieci zamieszkałcyh z klientem',
    'Teenhome': 'liczba nastolatków zaamieszkałych z klientem',
    'Income': 'roczny dochód gospodarstwa klienta',
    'MntFishProducts': 'wydatki na produkty rybne w przeciągu ostatnich dwóch lat',
    'MntMeatProducts': 'wydatki na produkty mięsne w przeciągu ostatnich dwóch lat',
    'MntFruits': 'wydatki na owoce w przeciągu ostatnich dwóch lat',
    'MntSweetProducts': 'wydatki na słodycze w przeciągu ostatnich dwóch lat',
    'MntWines': 'wydatki na wino w przeciągu ostatnich dwóch lat',
    'MntGoldProds': 'wydatki na wyroby ze złota w przeciągu ostatnich dwóch lat',
    'NumDelasPurchases': 'liczba zakupów ze zniżką',
    'NumCatalogPurchases': 'liczba zakupów z wykorzystaniem katalogu',
    'NumStorePurchases': 'liczba zakupów wykonanych bezpośrednio w sklepie',
    'NumWebPurchases': 'liczba zakupów dokonoanych przez stronę internetową',
    'NumWebVisitsMonth': 'liczba wizyt na stronie internetowej w przeciągu ostatniego miesiąca',
    'Recency': 'liczba dni od ostaniego zakupu',
    'Z_CostContact': '?',
    'Year_Birth': 'rok urodzenia klienta',
    }

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=mp['dropout_loss'],
        x=mp['variable']
    ))

    fig.update_layout(
        title='Wykres ważności zmiennych',
        xaxis=dict(title='Cechy'),
        yaxis=dict(title='Ważność')
    )

    st.plotly_chart(fig,use_container_width=True)

    tabs_names = list(mp["variable"].head(vips))

    # if 'pdp' not in st.session_state:
    #     st.session_state.pdp = xai.pdp(st.session_state.exp,list(st.session_state.mp["variable"]))
    #     st.session_state.pdp_cat = xai.pdp_cat(st.session_state.exp,list(st.session_state.mp["variable"]))

    with st.spinner("Generowanie wyników analizy..."):
        def make_pdp_plot(pdp_val, i):
            df = pdp_val[pdp_val["_vname_"]==tabs_names[i]]
            colors = ['red' if val < max(df['_yhat_'])-max(df['_yhat_'])*0.1 else 'green' for val in df['_yhat_']]
            fig = go.Figure()

            for i in range(len(df) - 1):
                fig.add_trace(go.Scatter(
                    x=df['_x_'].iloc[i:i+2],
                    y=df['_yhat_'].iloc[i:i+2],
                    mode='lines',
                    line=dict(color=colors[i]),
                    showlegend=False
                ))

            fig.update_layout(
                title='Line Plot',
                xaxis=dict(title='Wartość'),
                yaxis=dict(title='Prawdopodobieństwo')
            )

            return fig

        def make_pdp_cat_plot(pdp_val, i):
            df = pdp_val[pdp_val["_vname_"]==tabs_names[i]]
            df = df.sort_values(by="_yhat_", ascending = False)

            fig = go.Figure()

            fig.add_trace(go.Bar(
                y=df['_yhat_'],
                x=df['_x_']
            ))

            fig.update_layout(
                title='Bar Plot',
                xaxis=dict(title='Wartość'),
                yaxis=dict(title='Prawdopodobieństwo')
            )

            return fig

        tabs = st.tabs(tabs_names)

        n = 0
        for i in tabs:
            with i:
                c1,c2,c3 = st.columns([1,5,1])
                with c2:
                    if tabs_names[n] in categories:
                        st.plotly_chart(make_pdp_cat_plot(st.session_state.pdp_cat,n),use_container_width=True)
                    else:
                        st.plotly_chart(make_pdp_plot(st.session_state.pdp,n),use_container_width=True)
            n=n+1


        def make_target(n):
            if tabs_names[n] in categories:
                df = st.session_state.pdp_cat[st.session_state.pdp_cat["_vname_"]==tabs_names[n]]
                max_index = df['_yhat_'].idxmax()
                cat = df.loc[max_index, '_x_']
                return f"{desc_dict.get(tabs_names[n])} o wartości {cat}"
            else:
                df = st.session_state.pdp[st.session_state.pdp["_vname_"]==tabs_names[n]]
                top_10 = df['_yhat_'].quantile(0.9)
                top_10_df = df[df['_yhat_'] >= top_10]
                note = f"{desc_dict.get(tabs_names[n])} z przedziału {round(min(top_10_df['_x_']),2)}-{max(top_10_df['_x_'])}"
                return note

        st.header("Proponowana grupa docelowa:")
        n=0
        for i in range(vips):
            st.write(make_target(n))
            n=n+1