FROM nginx:1.31.0-alpine

COPY site /data/www/dagcellent
COPY k8s/nginx.conf /etc/nginx
