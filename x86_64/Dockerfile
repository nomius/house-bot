# base.docker
FROM python:alpine as builder
RUN apk add build-base libffi libffi-dev openssl openssl-dev
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python:alpine
RUN apk add openssl
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
WORKDIR /app
COPY bot.py config.py ./
RUN chmod 0755 bot.py
CMD [ "./bot.py" ]

