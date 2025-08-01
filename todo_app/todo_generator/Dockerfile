FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wiki_todo_generator.py .

CMD ["python", "-u", "wiki_todo_generator.py"]