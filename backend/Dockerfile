FROM python:3.11-slim

COPY requirements.txt entrypoint.sh /
COPY api /src
RUN chmod +x /entrypoint.sh
RUN pip3 install --no-cache-dir --upgrade -r /requirements.txt
WORKDIR /src
EXPOSE 8000
CMD ["/entrypoint.sh"]

