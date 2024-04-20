import dalex as dx
import pickle as pkl
import data_prep
import pandas as pd
from sklearn.model_selection import train_test_split
    
def build_exp():

    xgb = pkl.load(open("models/xgb.pkl", 'rb'))

    data = pd.read_csv("marketing_campaign.csv", sep = ";")
    X = data.drop("Response", axis=1)
    y = data["Response"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state = 2115)

    exp = dx.Explainer(xgb, X_train, y_train, model_type="classification")
    return exp

def vip(exp):
    mp = exp.model_parts()
    return mp.result

def pdp(exp, vars):
    pdp = exp.model_profile(variables = vars)
    return pdp.result