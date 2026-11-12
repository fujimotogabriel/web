from flask import Flask, render_template, request, redirect, url_for, flash
from contextlib import contextmanager
import pymysql
from dotenv import load_dotenv
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/personagens")
def personagens():
    return render_template("personagens.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        sugestao = request.form.get('sugestao').strip()
        titulo = request.form.get('titulo').strip()
        dia = datetime.now()
        dia = dia.strftime("%Y-%m-%d")

        if email and sugestao:
            with get_conn() as conn:
                with conn.cursor() as cur:

                    cur.execute("select * from sugestao where sug_sugestao like %s", f'%{sugestao}%')
                    if not cur.fetchone():
                        cur.execute(
                        "insert into sugestao (sug_email, sug_titulo, sug_sugestao, sug_data) values(%s, %s, %s, %s)", (email, titulo, sugestao, dia)
                        )
                    else:
                        flash("Sugestão já existe!")
                    
        return redirect(url_for("cadastro"))

    return render_template("cadastro.html")

@app.route("/listar")
def listar():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("select sug_id, sug_titulo, sug_sugestao, date_format(sug_data, '%d/%m/%Y') as sug_data from sugestao")
            sugestoes = cur.fetchall()
            
    return render_template("listar.html", sugestoes=sugestoes)

@contextmanager
def get_conn():

    load_dotenv()

    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        cursorclass=pymysql.cursors.DictCursor,
        connect_timeout=5
    )

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()