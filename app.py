from flask import Flask, render_template, request
from contextlib import contextmanager
import pymysql
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/personagens")
def chars():
    return render_template("personagens.html")

@app.route("/cadastro", methods=['GET', 'POST'])
def contato():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        sugestao = request.form.get('sugestao').strip()

        """if email and sugestao:
            with get_conn() as conn:
                with conn.cursor as cur:
                    cursor.execute(
                        "insert into sugestao (sug_email, sug_sugestao) values(%s, %s)", email, sugestao
                    )"""
        return redirect(url_for("cadastro"))

    return render_template("cadastro.html")

@contextmanager
def get_conn():

    load_dotenv()

    conn = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.get_env("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()