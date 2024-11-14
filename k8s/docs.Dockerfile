FROM nginx:1.27.2-alpine

COPY ../site /data/www/dagcellent
COPY nginx.conf /etc/nginx
