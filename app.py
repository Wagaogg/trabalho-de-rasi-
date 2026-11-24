import os
import mysql.connector
from flask import Flask

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST", "mysql"),
        database=os.environ.get("DB_NAME", "meu_banco"),
        user=os.environ.get("DB_USER", "flaskuser"),
        password=os.environ.get("DB_PASSWORD"),
    )

@app.route("/")
def home():
    return "<h1>Bem-vindo ao Flask no Docker</h1>"

@app.route("/sobre")
def sobre():
    return "<h1>Sobre o projeto</h1><p>Sistema escolar desenvolvido com Flask, MySQL e Apache.</p>"

@app.route("/contato")
def contato():
    return "<h1>Contato</h1><p>Projeto desenvolvido por Wagner.</p>"

@app.route("/alunos")
def alunos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT nome, curso FROM alunos")
    linhas = cur.fetchall()
    cur.close(); conn.close()
    itens = "".join(f"<li>{n} - {c}</li>" for n, c in linhas)
    return f"<h1>Lista de alunos</h1><ul>{itens}</ul>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)