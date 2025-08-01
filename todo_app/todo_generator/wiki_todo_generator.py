#!/usr/bin/env python3
import os
import requests
import psycopg2
from datetime import datetime
import sys
from dotenv import load_dotenv

load_dotenv()
DB_PORT = int(os.environ.get("POSTGRES_PORT"))
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

IS_LOCAL = "--local" in sys.argv
if IS_LOCAL:
    HOST= os.environ.get("LOCAL_POSTGRES_HOST")
else:
    HOST = os.environ.get("PROD_POSTGRES_HOST")

def get_random_wikipedia_url():
    """Get a random Wikipedia article URL by following redirect"""
    response = requests.head("https://en.wikipedia.org/wiki/Special:Random", 
                            allow_redirects=False)
    if response.status_code == 302:  # Redirect status code
        return response.headers.get("Location")
    return "https://en.wikipedia.org/wiki/Special:Random"

def insert_todo(url):
    """Insert a new todo into the database"""
    todo_text = f"Read {url}"

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=HOST,
        port=DB_PORT
    )

    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO todos (content) VALUES (%s);", (todo_text,))
        conn.commit()
        print(f"Added todo: {todo_text}")
    except Exception as e:
        print(f"Error inserting todo: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    print(f"Running Wikipedia todo generator at {datetime.now()}")
    url = get_random_wikipedia_url()
    insert_todo(url)