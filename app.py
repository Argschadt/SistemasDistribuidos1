import os
from datetime import date

from flask import Flask, flash, jsonify, redirect, render_template, request, url_for
import psycopg2
from psycopg2.extras import RealDictCursor


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret-key")


def env_or_default(name, default):
    value = os.getenv(name)
    if value is None:
        return default
    value = value.strip()
    return value if value else default


DB_CONFIG = {
    "host": env_or_default("PGHOST", "localhost"),
    "port": env_or_default("PGPORT", "5432"),
    "dbname": env_or_default("PGDATABASE", "postgres"),
    "user": env_or_default("PGUSER", "postgres"),
    "password": env_or_default("PGPASSWORD", "root"),
    "options": env_or_default("PGOPTIONS", "-c search_path=public"),
}

STATUS_OPTIONS = ["ativo", "inativo", "pendente", "bloqueado"]


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_people(search_term=None, limit=100):
    base_query = """
        SELECT id, nome, email, telefone, cidade, data_cadastro, status
        FROM public.pessoas
    """
    params = []

    if search_term:
        like_term = f"%{search_term}%"
        base_query += """
            WHERE CAST(id AS TEXT) ILIKE %s
               OR nome ILIKE %s
               OR email ILIKE %s
               OR COALESCE(telefone, '') ILIKE %s
               OR COALESCE(cidade, '') ILIKE %s
               OR COALESCE(status, '') ILIKE %s
        """
        params.extend([like_term] * 6)

    base_query += " ORDER BY id DESC LIMIT %s"
    params.append(limit)

    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(base_query, params)
            return cursor.fetchall()


def fetch_person(person_id):
    with get_connection() as connection:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(
                """
                SELECT id, nome, email, telefone, cidade, data_cadastro, status
                FROM public.pessoas
                WHERE id = %s
                """,
                (person_id,),
            )
            return cursor.fetchone()


def create_person_record(nome, email, telefone=None, cidade=None, status="ativo", data_cadastro=None):
    if data_cadastro is None:
        data_cadastro = date.today()

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.pessoas (nome, email, telefone, cidade, data_cadastro, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (nome, email, telefone, cidade, data_cadastro, status),
            )
            person_id = cursor.fetchone()[0]
        connection.commit()

    return person_id


def person_to_dict(person):
    return {
        "id": person["id"],
        "nome": person["nome"],
        "email": person["email"],
        "telefone": person["telefone"],
        "cidade": person["cidade"],
        "data_cadastro": person["data_cadastro"].isoformat() if person["data_cadastro"] else None,
        "status": person["status"],
    }


@app.route("/")
def index():
    search = request.args.get("q", "").strip()
    db_error = None

    try:
        people = fetch_people(search_term=search or None)
    except psycopg2.Error as exc:
        people = []
        db_error = str(exc).strip()

    return render_template(
        "index.html",
        people=people,
        search=search,
        status_options=STATUS_OPTIONS,
        total_shown=len(people),
        db_error=db_error,
    )


@app.route("/api/pessoas", methods=["GET"])
def api_list_people():
    search = request.args.get("q", "").strip()
    limit = request.args.get("limit", "100").strip()

    try:
        limit_value = max(1, min(int(limit), 1000))
    except ValueError:
        limit_value = 100

    try:
        people = fetch_people(search_term=search or None, limit=limit_value)
        return jsonify(
            {
                "count": len(people),
                "results": [person_to_dict(person) for person in people],
            }
        )
    except psycopg2.Error as exc:
        return jsonify({"error": str(exc).strip()}), 500


@app.route("/pessoas", methods=["POST"])
def create_person():
    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    telefone = request.form.get("telefone", "").strip() or None
    cidade = request.form.get("cidade", "").strip() or None
    status = request.form.get("status", "ativo").strip()
    data_cadastro = date.today()

    if not nome or not email:
        flash("Nome e e-mail são obrigatórios.")
        return redirect(url_for("index"))

    try:
        person_id = create_person_record(nome, email, telefone, cidade, status, data_cadastro)

        flash(f"Pessoa cadastrada com sucesso. ID: {person_id}")
    except psycopg2.Error as exc:
        flash(f"Erro ao salvar no banco: {str(exc).strip()}")

    return redirect(url_for("index"))


@app.route("/api/pessoas", methods=["POST"])
def api_create_person():
    payload = request.get_json(silent=True) or request.form

    nome = str(payload.get("nome", "")).strip()
    email = str(payload.get("email", "")).strip()
    telefone = str(payload.get("telefone", "")).strip() or None
    cidade = str(payload.get("cidade", "")).strip() or None
    status = str(payload.get("status", "ativo")).strip() or "ativo"

    if not nome or not email:
        return jsonify({"error": "Nome e e-mail são obrigatórios."}), 400

    try:
        person_id = create_person_record(nome, email, telefone, cidade, status)
        return jsonify(
            {
                "message": "Pessoa cadastrada com sucesso.",
                "id": person_id,
            }
        ), 201
    except psycopg2.Error as exc:
        return jsonify({"error": str(exc).strip()}), 500


@app.route("/pessoas/<int:person_id>/editar", methods=["GET", "POST"])
def edit_person(person_id):
    try:
        person = fetch_person(person_id)
        if not person:
            flash("Pessoa não encontrada.")
            return redirect(url_for("index"))
    except psycopg2.Error as exc:
        flash(f"Erro ao carregar pessoa: {str(exc).strip()}")
        return redirect(url_for("index"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip() or None
        cidade = request.form.get("cidade", "").strip() or None
        status = request.form.get("status", "ativo").strip()

        if not nome or not email:
            flash("Nome e e-mail são obrigatórios.")
            return redirect(url_for("edit_person", person_id=person_id))

        try:
            with get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE public.pessoas
                        SET nome = %s,
                            email = %s,
                            telefone = %s,
                            cidade = %s,
                            status = %s
                        WHERE id = %s
                        """,
                        (nome, email, telefone, cidade, status, person_id),
                    )
                connection.commit()

            flash("Pessoa atualizada com sucesso.")
        except psycopg2.Error as exc:
            flash(f"Erro ao atualizar no banco: {str(exc).strip()}")
        return redirect(url_for("index"))

    return render_template("edit.html", person=person, status_options=STATUS_OPTIONS)


@app.route("/pessoas/<int:person_id>/excluir", methods=["POST"])
def delete_person(person_id):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM public.pessoas WHERE id = %s", (person_id,))
            connection.commit()

        flash("Pessoa excluída com sucesso.")
    except psycopg2.Error as exc:
        flash(f"Erro ao excluir do banco: {str(exc).strip()}")

    return redirect(url_for("index"))


@app.route("/api/pessoas/<int:person_id>", methods=["DELETE"])
def api_delete_person(person_id):
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM public.pessoas WHERE id = %s", (person_id,))
            connection.commit()

        return jsonify({"message": "Pessoa excluída com sucesso.", "id": person_id})
    except psycopg2.Error as exc:
        return jsonify({"error": str(exc).strip()}), 500


@app.route("/saude")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True, threaded=True)
