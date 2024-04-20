# select image
FROM python:3.10-slim
LABEL authors="Michciak"

# install required packages
RUN pip install requests pandas sqlalchemy pymysql cryptography

# change working directory
WORKDIR /app

# copy files
COPY . /app

# expose port 5000
EXPOSE 5000

# run api
#CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "5000"]