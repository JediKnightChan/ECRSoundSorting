FROM node:lts-alpine as builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install --force
COPY frontend .
RUN npm run build


FROM nginx:stable-alpine as production-stage
COPY --from=builder /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.conf /etc/nginx/conf.d

FROM nginx:stable-alpine as development-stage
COPY --from=builder /app/dist /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx_http.conf /etc/nginx/conf.d
