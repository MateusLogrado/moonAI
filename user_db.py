import sqlite3
from datetime import datetime

def inicializar():
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
                id TEXT PRIMARY KEY,
                nome TEXT,
                primeira_vez TEXT,
                apelido TEXT DEFAULT NULL,
                interacoes INTEGER DEFAULT 0
                )
    """)

    conn.commit()
    conn.close()

def inserirUsuario(id, nome):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    data = datetime.now().strftime('%D-%m-%Y %H:%M:%S')

    cursor.execute("""
    INSERT OR IGNORE INTO usuarios (id, nome, primeira_vez) VALUES (?, ?, ?)
    """, (id, nome, data))
    conn.commit()

    conn.close()

def incrementarInteracoes(id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios SET interacoes = interacoes+1 WHERE id = ?
    """, (id,))
    conn.commit()

    conn.close()

def buscarUsuario(id):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM usuarios WHERE id = ?
    """, (id,))
    resultado = cursor.fetchone()

    conn.close()

    return resultado

def atualizarApelido(id, apelido):
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE usuarios SET apelido = ? WHERE id = ?
    """, (apelido, id))
    conn.commit()

    conn.close()