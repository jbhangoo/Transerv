FROM python:3.13-slim

# install dependencies
COPY requirements.txt /
RUN pip3 install --upgrade pip
RUN pip3 install -r /requirements.txt

# Set up application in its own directory
COPY . /app
WORKDIR /app

# This must match the port in gunicorn configuration file
EXPOSE 8080

CMD ["gunicorn","--config", "gunicorn.py", "app:app"]
