FROM node:23-alpine3.19 AS builder
ARG DEFAULT_PORT GOOGLE_ANALYTICS
ENV DEFAULT_PORT=$DEFAULT_PORT
ENV GOOGLE_ANALYTICS=$GOOGLE_ANALYTICS

COPY web /app
WORKDIR /app
RUN yarn install && yarn build

# production environment
FROM nginx:stable-alpine-slim AS web
ARG DEFAULT_PORT
ENV DEFAULT_PORT=$DEFAULT_PORT
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./entrypoint.sh /entrypoint.sh
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["sh", "/entrypoint.sh"]
