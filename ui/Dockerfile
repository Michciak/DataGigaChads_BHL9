# select image
FROM python:3.10.14-slim

# install required packages
RUN pip install --upgrade pip
RUN pip install scikit-learn==1.4.2 pandas==2.2.2 sqlalchemy==2.0.29 plotly==5.21.0 streamlit==1.33.0 dalex imblearn pymysql cryptography xgboost

# change working directory
WORKDIR /app

# copy files
COPY . /app

# expose port 5000
EXPOSE 5000

# run web-app
CMD ["streamlit", "run", "Wprowadzenie.py", "--server.port", "5000", "--server.enableXsrfProtection", "false"]