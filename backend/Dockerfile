FROM python:3.10.8-bullseye

#Set the working directory
WORKDIR /app

#Set the environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Set Python path
ENV PYTHONPATH "${PYTHONPATH}:/app"

#Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy the project
COPY . .

WORKDIR /app/app
