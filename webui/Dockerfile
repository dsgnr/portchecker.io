FROM node:alpine
WORKDIR /srv
COPY .yarn/ ./.yarn
COPY .yarnrc.yml yarn.lock package.json ./
RUN yarn install && yarn add webpack
COPY . ./webui
WORKDIR /webui
EXPOSE 8080
CMD ["yarn", "run", "build"]
