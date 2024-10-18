FROM python:3.11

# Install dependencies
RUN pip install pandas Flask flask_cors gunicorn vertexai google-generativeai PyPDF2 openpyxl

# Copy the source code into the container
COPY src/ /app

# Set the working directory
WORKDIR /app

# Expose the necessary port
ENV PORT 8080

# Command to run the application using gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
