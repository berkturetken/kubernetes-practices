FROM python:3.11-alpine

WORKDIR /app

COPY main.py .

# -u flag is used to run the Python script in unbuffered mode
# which is useful for logging output in real-time.
CMD ["python", "-u", "main.py"]