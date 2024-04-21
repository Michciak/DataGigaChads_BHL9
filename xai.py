import dalex as dx
import pickle as pkl
import data_prep
import pandas as pd
from sklearn.model_selection import train_test_split
    
def build_exp(model_name: str, data: pd.DataFrame = None):

    xgb = pkl.load(open(model_name, 'rb'))

    if data is None:
        # only for development purposes
        data = pd.read_csv("marketing_campaign.csv", sep = ";")

    #data["Dt_Customer"] = pd.to_datetime(data["Dt_Customer"]).dt.year
    
    data["Income"] = data["Income"].fillna(data["Income"].median())

    #data reliability check
    #data = data.drop(columns=["ID", "Z_costcontact", "Z_Revenue"], axis=1)
    data = data[data["Year_Birth"]>1930]
    data = data[data["Income"]<200000]
    martial_ac = ["Single","Together","Married","Divorced","Widow"]
    data = data[data["Marital_Status"].isin(martial_ac)]

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

def pdp_cat(exp,vars):
    pdp = exp.model_profile(variable_type = "categorical", variables = vars)
    return pdp.result