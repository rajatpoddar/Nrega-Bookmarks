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

# App run karne ki command
CMD ["python", "app.py"]