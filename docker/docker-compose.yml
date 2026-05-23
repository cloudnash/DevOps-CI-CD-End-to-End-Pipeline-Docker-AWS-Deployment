version: "3.9"

# ─────────────────────────────────────────────────────────────────────────────
# Docker Compose — Local Development Environment
# Usage: docker-compose up --build
# ─────────────────────────────────────────────────────────────────────────────

services:

  app:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    container_name: devops-showcase-app
    ports:
      - "5000:5000"
    environment:
      - ENVIRONMENT=development
      - APP_VERSION=1.0.0
    volumes:
      - ../app:/home/appuser/app   # live-reload during development
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
    networks:
      - devops-net

  # Optional: Nginx reverse proxy (uncomment to use)
  # nginx:
  #   image: nginx:alpine
  #   container_name: devops-nginx
  #   ports:
  #     - "80:80"
  #   volumes:
  #     - ./nginx.conf:/etc/nginx/nginx.conf:ro
  #   depends_on:
  #     - app
  #   networks:
  #     - devops-net

networks:
  devops-net:
    driver: bridge
