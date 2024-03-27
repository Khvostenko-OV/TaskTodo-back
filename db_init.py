import psycopg2
from werkzeug.security import generate_password_hash

from config import DB_NAME, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD


if __name__ == '__main__':

    conn = psycopg2.connect(database='postgres', host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    conn.autocommit = True

    cur.execute(f"SELECT datname FROM pg_database WHERE datname = '{DB_NAME}';")
    res = cur.fetchone()
    if not res:
        print(f'--- Create database: {DB_NAME}')
        cur.execute(f'CREATE DATABASE {DB_NAME};')

    cur.close()
    conn.close()

    conn = psycopg2.connect(database=DB_NAME, host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()

    print('--- Drop tables if exist: users, tasks')
    cur.execute(f'DROP TABLE IF EXISTS users;')
    cur.execute(f'DROP TABLE IF EXISTS tasks;')
    conn.commit()

    print('--- Create tables: users, tasks')
    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(32) NOT NULL UNIQUE,
            email VARCHAR(128) NOT NULL DEFAULT 'test@test.com',
            password_hash VARCHAR(192) NOT NULL,
            is_admin BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        ); 
    ''')

    cur.execute(f'''
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            author VARCHAR(40) NOT NULL,
            email VARCHAR(128) NOT NULL,
            text TEXT NOT NULL,
            done BOOLEAN DEFAULT FALSE,
            changed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        );
    ''')

    conn.commit()

    print('--- Create admin user')
    cur.execute(f'''
        INSERT INTO users (username, email, password_hash, is_admin)
        VALUES ('admin', 'admin@admin.com', '{generate_password_hash('123')}', TRUE);
    ''')

    conn.commit()
    print('------ Done')
    cur.close()
    conn.close()
