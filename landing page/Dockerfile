FROM node:10-alpine as builder

WORKDIR /app

COPY package.json package.json
COPY package-lock.json package-lock.json

RUN npm ci

COPY . .

RUN npm run build:prod

FROM jroslaniec/spa-nginx:0.5.0

COPY --from=builder /app/dist /www/data
