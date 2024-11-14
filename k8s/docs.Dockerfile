FROM nginx:1.27.2-alpine

COPY site /data/www/dagcellent
COPY k8s/nginx.conf /etc/nginx
