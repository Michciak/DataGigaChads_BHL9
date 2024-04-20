import dalex as dx
import pickle as pkl
import data_prep
import pandas as pd

def build_exp():
    rf = pkl.load(open("models/rf1.pkl", 'rb'))
    df = pd.read_csv("marketing_campaign.csv", sep=";")

    x_train, y_train, x_test, y_test = data_prep.prep_data(df)
    exp = dx.Explainer(rf, x_train, y_train, model_type="classification")
    return exp

def vip(exp):
    mp = exp.model_parts()
    return mp.result

def pdp(exp, vars):
    pdp = exp.model_profile(variables = vars)
    return pdp.result