FROM python:3.9-slim
RUN pip install mysql-connector-python
COPY . /app
WORKDIR /app
CMD python client.py
