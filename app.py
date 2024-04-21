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
        'AcceptedCmp5',
        'Dt_Customer'
    ]

if 'data' not in st.session_state:
    st.session_state.data = pd.read_csv("marketing_campaign.csv", sep = ";")

st.set_page_config(page_title="Sentiment Analysis", layout="wide")
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

if 'db_b' not in st.session_state:
    st.session_state.db_b = False

if 'new_df' not in st.session_state:
    st.session_state.new_df = None
    st.session_state.new_df_ready = False

col_db, input_col = st.columns([10,2])
with input_col:
    st.markdown("""
                    <style>
                    button {
                        height: auto;
                        padding-top: 10px !important;
                        padding-bottom: 10px !important;
                    }</style>""", unsafe_allow_html=True, )
    db_button = st.button('Manage Data', use_container_width=True)
    if db_button:
        st.session_state.db_b = not st.session_state.db_b

if st.session_state.db_b:
    with col_db:
        file_up_col, file_push_col = st.columns([7,2])
        with file_up_col:
            loaded_csv = st.file_uploader('Upload .csv file', type='csv')
            if loaded_csv is not None:
                st.session_state.new_df = pd.read_csv(loaded_csv)
                st.session_state.new_df_ready = True
        with file_push_col:
            st.write('')
            st.button('Push file to database', on_click=push_to_db, use_container_width=True, args=(st.session_state.new_df,), disabled=not st.session_state.new_df_ready)
            st.session_state.data = st.button('Load file from database', on_click=pull_from_db, use_container_width=True)

c1,c2,c3,c4,c5 = st.columns(5)
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

st.divider()

c1,c2,c3,c4,c5 = st.columns(5)
with c2:
    st.metric("#### Sukces poprzedniej kamapnii", f"{round(st.session_state.data['Response'].sum()/len(st.session_state.data)*100,2)}%")
with c4:
    st.metric("#### Prognozowany sukces kamapnii", 100, delta=1000)

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

fig = go.Figure()

fig.add_trace(go.Bar(
    y=mp['dropout_loss'],
    x=mp['variable']
))

fig.update_layout(
    title='Bar Plot',
    xaxis=dict(title='Values'),
    yaxis=dict(title='Labels')
)

st.plotly_chart(fig,use_container_width=True)

tabs_names = list(mp["variable"].head(vips))

if 'pdp' not in st.session_state:
    st.session_state.pdp = xai.pdp(exp,list(st.session_state.mp["variable"]))
    st.session_state.pdp_cat = xai.pdp_cat(exp,list(st.session_state.mp["variable"]))

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
        xaxis=dict(title='Values'),
        yaxis=dict(title='Labels')
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
        return f"{tabs_names[n]} o wartości {cat}"
    else:
        df = st.session_state.pdp[st.session_state.pdp["_vname_"]==tabs_names[n]]
        top_10 = df['_yhat_'].quantile(0.9)
        top_10_df = df[df['_yhat_'] >= top_10]
        note = f"{tabs_names[n]} z przedziału {round(min(top_10_df['_x_']),2)}-{max(top_10_df['_x_'])}"
        return note

st.header("Proponowana grupa docelowa:")
n=0
for i in range(vips):
    st.write(make_target(n))
    n=n+1