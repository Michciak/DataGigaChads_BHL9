# select image
FROM python:3.10-slim

# install required packages
RUN pip install requests streamlit pandas

# change working directory
WORKDIR /app

# copy files
COPY . /app

# expose port 5000
EXPOSE 5000

# run web-app
#CMD ["streamlit", "run", "app.py", "--server.port", "5000", "--server.enableXsrfProtection", "false"]