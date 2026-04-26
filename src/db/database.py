import os
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor

# Leemos la URL de Supabase desde las variables de entorno
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    if DATABASE_URL:
        # Añadimos parámetros extra para que el pooler identifique tu base de datos
        conn = psycopg2.connect(
            DATABASE_URL, 
            cursor_factory=RealDictCursor,
            sslmode='require',
            connect_timeout=10,
            options="-c search_path=public" # Esto ayuda a veces con el Pooler
        )
        return conn
    else:
        # CONEXIÓN LOCAL (SQLite) para desarrollo
        db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'docusuite.db')
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        conn.execute('PRAGMA foreign_keys = ON')
        return conn

# Asegúrate de que las tablas se crean así para Postgres en database.py:
def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # En Postgres usamos SERIAL para IDs autoincrementales
    cur.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS proyectos (
        id SERIAL PRIMARY KEY,
        usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
        nombre TEXT NOT NULL,
        tipo TEXT NOT NULL,
        fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS documentos (
        id SERIAL PRIMARY KEY,
        id_proyecto INTEGER REFERENCES proyectos(id) ON DELETE CASCADE,
        usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
        titulo TEXT NOT NULL,
        autor TEXT,
        contenido_texto TEXT,
        fecha_modificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Base de datos sincronizada.")
