from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)


def get_connection():
    return pymysql.connect(
        host="db",
        user="clase",
        password="clase123",
        database="creditos",
        cursorclass=pymysql.cursors.DictCursor
    )


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando"
    }


@app.get("/prestamos")
def obtener_prestamos():

    conexion = get_connection()

    impago = request.args.get("impago")

    with conexion.cursor() as cursor:

        if impago is not None:

            cursor.execute(
                "SELECT * FROM clientes_credito WHERE impago=%s LIMIT 100",
                (impago,)
            )

        else:

            cursor.execute(
                "SELECT * FROM clientes_credito LIMIT 100"
            )

        prestamos = cursor.fetchall()

    conexion.close()

    return jsonify(prestamos)

@app.get("/prestamos/<int:id>")
def obtener_prestamo(id):

    conexion = get_connection()

    with conexion.cursor() as cursor:

        cursor.execute(
            "SELECT * FROM clientes_credito WHERE id=%s",
            (id,)
        )

        prestamo = cursor.fetchone()

    conexion.close()

    if prestamo is None:

        return jsonify({
            "error": "Prestamo no encontrado"
        }), 404

    return jsonify(prestamo)

@app.get("/estadisticas")
def obtener_estadisticas():

    conexion = get_connection()

    with conexion.cursor() as cursor:

        cursor.execute("""
            SELECT
                COUNT(*) as total_prestamos,
                AVG(prima) as prima_media,
                SUM(impago) as total_impagos
            FROM clientes_credito
        """)

        estadisticas = cursor.fetchone()

    conexion.close()

    return jsonify(estadisticas)

@app.post("/prestamos")
def crear_prestamo():

    datos = request.json

    conexion = get_connection()

    with conexion.cursor() as cursor:

        cursor.execute(
            """
            INSERT INTO clientes_credito
            (edad, ingresos, monto_inicial)
            VALUES (%s, %s, %s)
            """,
            (
                datos["edad"],
                datos["ingresos"],
                datos["monto_inicial"]
            )
        )

        conexion.commit()

    conexion.close()

    return jsonify({
        "mensaje": "Prestamo creado correctamente"
    }), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)