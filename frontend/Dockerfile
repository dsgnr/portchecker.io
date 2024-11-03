FROM node:23-alpine3.19 as builder
ARG GOOGLE_ANALYTICS ADSENSE_VERIFICATION
ENV GOOGLE_ANALYTICS=$GOOGLE_ANALYTICS
ENV ADSENSE_VERIFICATION=$ADSENSE_VERIFICATION

COPY web /app
WORKDIR /app
RUN yarn install && yarn build

# production environment
FROM nginx:stable-alpine-slim
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
