from flask import Flask, jsonify, request
import pymysql
import requests

app = Flask(__name__)


def get_connection():
    try:
        return pymysql.connect(
            host="db",
            user="clase",
            password="clase123",
            database="creditos",
            cursorclass=pymysql.cursors.DictCursor
        )

    except pymysql.MySQLError as e:
        print(f"Error de conexión: {e}")
        return None


@app.get("/")
def inicio():
    return {
        "mensaje": "API funcionando"
    }


@app.get("/prestamos")
def obtener_prestamos():

    conexion = get_connection()

    if conexion is None:
        return jsonify({
            "error": "No se pudo conectar con la base de datos"
        }), 500

    try:

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

        return jsonify(prestamos)

    except pymysql.MySQLError as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:
        conexion.close()

@app.get("/prestamos/<int:id>")
def obtener_prestamo(id):

    conexion = get_connection()

    if conexion is None:

        return jsonify({
            "error": "No se pudo conectar con la base de datos"
        }), 500

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                "SELECT * FROM clientes_credito WHERE id=%s",
                (id,)
            )

            prestamo = cursor.fetchone()

        if prestamo is None:

            return jsonify({
                "error": "Prestamo no encontrado"
            }), 404

        return jsonify(prestamo)

    except pymysql.MySQLError as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        conexion.close()

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

    if not request.json:

        return jsonify({
            "error": "JSON no proporcionado"
        }), 400

    datos = request.json

    if (
        "edad" not in datos or
        "ingresos" not in datos or
        "monto_inicial" not in datos
    ):

        return jsonify({
            "error": "Faltan campos obligatorios"
        }), 400

    conexion = get_connection()

    if conexion is None:

        return jsonify({
            "error": "No se pudo conectar con la base de datos"
        }), 500

    try:

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

        return jsonify({
            "mensaje": "Prestamo creado correctamente"
        }), 201

    except pymysql.MySQLError as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        conexion.close()

@app.put("/prestamos/<int:row_id>")
def actualizar_prestamo(row_id):

    if not request.json:

        return jsonify({
            "error": "JSON no proporcionado"
        }), 400

    datos = request.json

    conexion = get_connection()

    if conexion is None:

        return jsonify({
            "error": "No se pudo conectar con la base de datos"
        }), 500

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                UPDATE clientes_credito
                SET edad=%s,
                    ingresos=%s,
                    monto_inicial=%s
                WHERE row_id=%s
                """,
                (
                    datos["edad"],
                    datos["ingresos"],
                    datos["monto_inicial"],
                    row_id
                )
            )

            conexion.commit()

            if cursor.rowcount == 0:

                return jsonify({
                    "error": "Prestamo no encontrado"
                }), 404

        return jsonify({
            "mensaje": "Prestamo actualizado correctamente"
        })

    except pymysql.MySQLError as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        conexion.close()

@app.delete("/prestamos/<int:row_id>")
def eliminar_prestamo(row_id):

    conexion = get_connection()

    if conexion is None:

        return jsonify({
            "error": "No se pudo conectar con la base de datos"
        }), 500

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM clientes_credito
                WHERE row_id=%s
                """,
                (row_id,)
            )

            conexion.commit()

            if cursor.rowcount == 0:

                return jsonify({
                    "error": "Prestamo no encontrado"
                }), 404

        return jsonify({
            "mensaje": "Prestamo eliminado correctamente"
        })

    except pymysql.MySQLError as e:

        return jsonify({
            "error": str(e)
        }), 500

    finally:

        conexion.close()


@app.get("/indicadores-pobreza")
def obtener_indicadores_pobreza():

    try:

        url = (
            "https://api.worldbank.org/v2/country/ESP/"
            "indicator/SI.POV.GINI?format=json"
        )

        respuesta = requests.get(url)

        respuesta.raise_for_status()

        datos = respuesta.json()

        for registro in datos[1]:

            if registro["value"] is not None:

                return jsonify({
                    "pais": registro["country"]["value"],
                    "indicador": registro["indicator"]["value"],
                    "año": registro["date"],
                    "valor": registro["value"]
                })

    except requests.RequestException as e:

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)