FROM node:alpine

COPY package.json yarn.lock ./
RUN yarn install && yarn global add webpack
COPY . ./webui
WORKDIR /webui
EXPOSE 8080
CMD ["yarn", "run", "build"]
