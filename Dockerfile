FROM python:3.8-slim AS builder

WORKDIR /app

COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Create the Gunicorn configuration file
RUN echo 'workers = 4' >gunicorn_config.py

# Stage 2: Use Nginx as a reverse proxy
FROM nginx:1.21.3-alpine

# Copy Gunicorn-based Flask application from the builder stage
COPY --from=builder /app /app

# Remove default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
