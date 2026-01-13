FROM node:25-alpine3.22 AS builder
ARG API_URL DEFAULT_HOST DEFAULT_PORT GOOGLE_ANALYTICS
ENV API_URL=$API_URL
ENV DEFAULT_HOST=$DEFAULT_HOST
ENV DEFAULT_PORT=$DEFAULT_PORT
ENV GOOGLE_ANALYTICS=$GOOGLE_ANALYTICS

COPY web /app
WORKDIR /app
RUN yarn install && yarn build

# production environment
FROM nginx:stable-alpine-slim AS web
ARG API_URL DEFAULT_HOST DEFAULT_PORT
ENV API_URL=$API_URL
ENV DEFAULT_HOST=$DEFAULT_HOST
ENV DEFAULT_PORT=$DEFAULT_PORT
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./entrypoint.sh /entrypoint.sh
COPY ./nginx/nginx.conf.template /etc/nginx/conf.d/default.conf.template
EXPOSE 80
CMD ["sh", "/entrypoint.sh"]
