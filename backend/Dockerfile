FROM python:3.12.7-alpine3.20
RUN apk update && apk add python3-dev \
                          gcc \
                          libc-dev \
                          libffi-dev
COPY requirements.txt entrypoint.sh /
COPY api /src
RUN chmod +x /entrypoint.sh
RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt
WORKDIR /src
EXPOSE 8000
CMD ["/entrypoint.sh"]

