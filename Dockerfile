# Base image
FROM python:3.9-slim

# Working directory set karo
WORKDIR /app

# Requirements file copy karke dependencies install karo
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Pura code copy karo
COPY . .

# Flask default port expose karo
EXPOSE 5000

# App ko production server (Gunicorn) ke through run karo
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]