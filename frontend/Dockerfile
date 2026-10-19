FROM nginx:alpine

# Copy our dashboard code into Nginx's default public directory
COPY index.html /usr/share/nginx/html/

# Copy a reverse proxy mapping configuration block so frontend traffic paths cleanly route down to the API
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
    } \
    location /api/ { \
        proxy_pass http://backend-service:5000/; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
