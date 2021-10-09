# base.docker
FROM arm64v8/python:alpine as builder
RUN apk add build-base libffi libffi-dev openssl openssl-dev
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM arm64v8/python:alpine
RUN apk add openssl
COPY --from=builder `python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'` `python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'`
WORKDIR /app
COPY bot.py config.py ./
RUN chmod 0755 bot.py
CMD [ "./bot.py" ]

