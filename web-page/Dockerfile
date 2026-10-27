# Lightweight static web server
FROM nginx:alpine

# Copy the web app into nginx's default web root
COPY index.html /usr/share/nginx/html/index.html

# nginx listens on port 80 inside the container
EXPOSE 80

# Simple health check
HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://localhost/ >/dev/null || exit 1

CMD ["nginx", "-g", "daemon off;"]
