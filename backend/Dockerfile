FROM python:3.12.7-alpine3.20 AS builder
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    python3-dev
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/pkgs -r /requirements.txt

FROM python:3.12.7-alpine3.20
COPY --from=builder /pkgs /usr/local
COPY entrypoint.sh .
COPY api /src
RUN chmod +x /entrypoint.sh
WORKDIR /src
EXPOSE 8000
CMD ["/entrypoint.sh"]
