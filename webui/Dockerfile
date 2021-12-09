FROM node:alpine

# ALlows the user to define a default port to populate the UI.
# Pass a desired value in your docker run/compose environment
ENV DEFAULT_PORT=$DEFAULT_PORT

COPY package.json yarn.lock ./
RUN yarn install && yarn global add webpack
COPY . ./webui
WORKDIR /webui
EXPOSE 8080
CMD ["yarn", "run", "build"]
