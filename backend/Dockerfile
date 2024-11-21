# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy all files in the backend folder, including requirements.txt
COPY . .

# Install dependencies using requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader -d /usr/local/share/nltk_data punkt

# Expose the backend port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
