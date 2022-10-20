FROM python:3.9.4

#Set the working directory
WORKDIR /app

#Set the environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Set Python path
ENV PYTHONPATH "${PYTHONPATH}:/src"

#Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

#Copy the project
COPY . .

WORKDIR /app/src