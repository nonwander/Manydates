FROM nginx:1.21.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ./compose/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

ENTRYPOINT ["nginx", "-g", "daemon off;"]