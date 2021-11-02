FROM node:lts-alpine3.14 

COPY package.json ./
COPY package-lock.json ./
RUN npm install --silent && yarn add -D webpack-cli
COPY . ./webui
WORKDIR /webui
EXPOSE 8080
CMD ["npm", "run", "build"]
