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

st.set_page_config(page_title="Sentiment Analysis", layout="wide")
st.title("Analiza kampanii marketingowej")
st.header("W oparciu o profilowanie klienta")

with st.sidebar:
    st.header("XD")

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

st.header("Najbardziej wpływowe cechy")
st.subheader("Na podstaiwe modelu AI")
mp = xai.vip(exp)
exclude_values = ["_baseline_","_full_model_"]
mp = mp.query('variable not in @exclude_values')

mp = mp.sort_values(by="dropout_loss", ascending=False).head(n=5)

fig = go.Figure()

#mp = mp.sort_values(by="dropout_loss", ascending=True)

# fig.add_trace(go.Bar(
#     x=mp['dropout_loss'],
#     y=mp['variable'],
#     orientation='h'
# ))

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

tabs_names = list(mp["variable"].head(5))
pdp = xai.pdp(exp,tabs_names)

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

t1,t2,t3,t4,t5 = st.tabs(tabs_names)
with t1:
    c1,c2,c3 = st.columns([1,5,1])
    with c2:
        st.plotly_chart(make_pdp_plot(pdp,0),use_container_width=True)
with t2:
    c1,c2,c3 = st.columns([1,5,1])
    with c2:
        st.plotly_chart(make_pdp_plot(pdp,1),use_container_width=True)
with t3:
    c1,c2,c3 = st.columns([1,5,1])
    with c2:
        st.plotly_chart(make_pdp_plot(pdp,2),use_container_width=True)
with t4:
    c1,c2,c3 = st.columns([1,5,1])
    with c2:
        st.plotly_chart(make_pdp_plot(pdp,3),use_container_width=True)
with t5:
    c1,c2,c3 = st.columns([1,5,1])
    with c2:
        st.plotly_chart(make_pdp_plot(pdp,4),use_container_width=True)