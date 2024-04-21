import streamlit as st
import xai as xai
import plotly.graph_objects as go
import plotly.express as px
from sklearn.base import BaseEstimator, TransformerMixin

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

st.title("Analiza kampanii marketingowej")
st.header("W oparciu o profilowanie klienta")

# with st.sidebar:
#     st.header("XD")

c1,c2,c3,c4,c5 = st.columns(5)
with c1:
    st.metric("Sukces kampanii nr 1", 1, delta=1)
with c2:
    st.metric("Sukces kampanii nr 2", 2, delta=-11)
with c3:
    st.metric("Sukces kampanii nr 3", 3, delta=22)
with c4:
    st.metric("Sukces kampanii nr 4", 4, delta=11)
with c5:
    st.metric("Sukces kampanii nr 5", 5, delta=16)

st.divider()

c1,c2,c3,c4,c5 = st.columns(5)
with c2:
    st.metric("Sukces poprzedniej kamapnii", 100, delta=1000)
with c4:
    st.metric("Prognozowany sukces kamapnii", 100, delta=1000)

st.divider()

st.title("Analiza profilu klienta")

st.write("Wybierz jaką liczbę cech chcesz uwzględnić:")
vips = st.slider("Liczba cech klienta",1,10,value=5)

st.header("Najbardziej wpływowe cechy")
st.subheader("Na podstawie modelu AI")
if 'mp' not in st.session_state:
    st.session_state.mp = xai.vip(exp)
    exclude_values = ["_baseline_","_full_model_"]
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
