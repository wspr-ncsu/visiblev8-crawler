from nginx:1.21

ENV BACKEND_HOST web_server
ENV BACKEND_PORT 80
ENV FRONTEND_HOST frontend
ENV FRONTEND_PORT 80

COPY ./nginx.conf /app/nginx.conf
RUN envsubst < /app/nginx.conf > /etc/nginx/nginx.conf
RUN rm -rf /app/

#COPY ./nginx.conf /etc/nginx/nginx.conf
#RUN cat /etc/nginx/nginx.conf
#RUN envsubst < /etc/nginx/nginx.conf > /etc/nginx/nginx.conf
#RUN /etc/nginx/nginx.conf
