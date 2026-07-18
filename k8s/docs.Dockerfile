FROM nginx:1.31.3-alpine

COPY site /data/www/dagcellent
COPY k8s/nginx.conf /etc/nginx
