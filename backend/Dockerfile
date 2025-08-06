# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files in the backend folder, including requirements.txt
COPY . .

# Install dependencies using requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt

# Install supervisord
RUN apt-get update && apt-get install -y supervisor && apt-get clean

# Expose the backend port
EXPOSE 5000

# Copy the supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run supervisord
CMD ["supervisord", "-n"]
