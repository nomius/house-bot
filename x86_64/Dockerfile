# base.docker
FROM python:alpine as builder
RUN apk add build-base libffi libffi-dev openssl openssl-dev
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip && \
	pip install --no-cache-dir -r requirements.txt && \
	cp -prf `python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'` /

FROM python:alpine
RUN apk add openssl
COPY --from=builder site-packages /site-packages
RUN rm -rf `python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'` && \
	mv /site-packages `python3 -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])'`
WORKDIR /app
COPY bot.py config.py ./
RUN chmod 0755 bot.py
CMD [ "./bot.py" ]

