FROM python:3.11

RUN pip install pandas Flask gunicorn vertexai google-generativeai PyPDF2 openpyxl

COPY src/ app/
WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app

# flask-simple-server
# export GOOGLE_APPLICATION_CREDENTIALS="/Users/hiroyuki/GoogleCloudPlatform/flask-firebase-sample/app-fukui-gen-ai-7c66629aaca5.json"
