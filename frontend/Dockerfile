FROM node:lts-alpine

WORKDIR /app

COPY ./babel.config.js .
COPY ./jsconfig.json .
COPY ./vue.config.js .

COPY package*.json ./
RUN npm install

COPY ./src ./src

RUN npm run build