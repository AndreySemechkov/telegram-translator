FROM alpine

WORKDIR /app/
RUN mkdir -p /app/templates/
COPY templates/* /app/templates/
COPY requirements.txt .
RUN apk update && apk add python3 py3-pip cairo curl
RUN python3 -m pip install -r requirements.txt
COPY *.py /app/
CMD [ "python3", "/app/flaskServer.py" ]
EXPOSE 5000
