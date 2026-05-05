FROM ubuntu:latest
RUN apt-get update && apt-get install -y gcc libmysqlclient-dev
COPY . /app
WORKDIR /app
# -lmysqlclient diletakkan di belakang untuk elak 'undefined reference'
RUN gcc -Wall -o server main.c -lpthread -lmysqlclient
CMD ["./server"]
