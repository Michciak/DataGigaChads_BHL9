import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

def prep_data(df):
    #transform columns
    df.columns = df.columns.str.lower()
    df["dt_customer"] = pd.to_datetime(df["dt_customer"]).dt.year

    #filling nan's in income
    df["income"] = df["income"].fillna(df["income"].median())

    #data reliability check
    df = df.drop(columns=["id", "z_costcontact", "z_revenue"])
    df = df[df["year_birth"]>1930]
    df = df[df["income"]<200000]
    martial_ac = ["Single","Together","Married","Divorced","Widow"]
    df = df[df["marital_status"].isin(martial_ac)]

    X = df.drop(columns="response", axis=1)

    numeric_features = X.select_dtypes(include=['number']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object']).columns.tolist()

    #one hot encoding
    encoder = OneHotEncoder(sparse_output=False,drop='first',handle_unknown='ignore')
    encoded_features = encoder.fit_transform(df[categorical_features])
    encoded_df = pd.DataFrame(encoded_features, columns=encoder.get_feature_names_out(categorical_features),index=df.index)

    #df.reset_index(drop=True, inplace=True)
    df.drop(columns=categorical_features, inplace=True)
    df = pd.concat([df, encoded_df], axis=1)

    #data split
    y = df["response"]
    X = df.drop(columns="response", axis=1)

    x_train, x_test, y_train, y_test = train_test_split(X,y, test_size=0.2)

    #scaling
    scaler = StandardScaler()
    x_train[numeric_features] = scaler.fit_transform(x_train[numeric_features])
    x_test[numeric_features] = scaler.transform(x_test[numeric_features])

    return x_train, y_train, x_test, y_test   