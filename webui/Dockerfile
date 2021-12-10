FROM node:alpine AS builder

COPY package.json yarn.lock ./
RUN yarn install && yarn global add webpack
COPY . ./app
WORKDIR /app
RUN yarn build

# production environment
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY --from=builder /app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
