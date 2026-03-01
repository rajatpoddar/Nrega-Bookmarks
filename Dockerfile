# Stage 1: Build Tailwind CSS
FROM node:18-alpine AS css-builder
WORKDIR /app
RUN npm install -g tailwindcss@3
COPY tailwind.config.js .
# Create directory structure and copy input
RUN mkdir -p static/css
COPY static/css/input.css ./static/css/input.css
COPY templates/ ./templates/
# Compile Tailwind classes used in HTML files
RUN tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.css --minify

# Stage 2: Final Python App
FROM python:3.9-slim
WORKDIR /app

# Requirements install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pura code copy karo
COPY . .

# Stage 1 se compiled CSS copy karo
COPY --from=css-builder /app/static/css/tailwind.css ./static/css/tailwind.css

# Flask default port expose karo
EXPOSE 5000

# App ko production server (Gunicorn) ke through run karo
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]