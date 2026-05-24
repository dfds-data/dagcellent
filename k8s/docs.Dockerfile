FROM nginx:1.31.1-alpine

COPY site /data/www/dagcellent
COPY k8s/nginx.conf /etc/nginx
