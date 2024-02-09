FROM node:20.5.0 as builder
ARG GOOGLE_ANALYTICS ADSENSE_VERIFICATION
ENV GOOGLE_ANALYTICS=$GOOGLE_ANALYTICS
ENV ADSENSE_VERIFICATION=$ADSENSE_VERIFICATION

COPY web/package.json ./
RUN yarn install && yarn global add webpack
COPY ./web ./app
WORKDIR /app
RUN yarn build

# production environment
FROM nginx:stable-alpine-slim
COPY --from=builder /app/dist /usr/share/nginx/html
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
