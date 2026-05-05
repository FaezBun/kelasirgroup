FROM ubuntu:latest
RUN apt-get update && apt-get install -y gcc
COPY . /app
WORKDIR /app
RUN gcc -o client client.c
CMD ["./client"]
