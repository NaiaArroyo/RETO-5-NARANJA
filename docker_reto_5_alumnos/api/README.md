# RETO-5-NARANJA
repositorio reto 5 equipo naranja

# API REST - Reto 5 Equipo Naranja

## Descripción

API REST desarrollada con Flask para la gestión de préstamos y seguros de protección de pagos del Reto 5.

La API permite consultar información almacenada en una base de datos MySQL y realizar operaciones CRUD sobre los registros de préstamos.

## Tecnologías utilizadas

- Python
- Flask
- MySQL
- PyMySQL
- Docker
- Postman
- Power BI

## Estructura del proyecto

```text
docker_reto_5_alumnos/
│
├── api/
│   └── main.py
│
├── loader/
│   └── load_data.py
│
├── datos/
│
└── docker-compose.yml
```

---

## Endpoints disponibles

### GET /

Comprueba que la API está funcionando correctamente.

#### Respuesta

```json
{
    "mensaje": "API funcionando"
}
```

---

### GET /prestamos

Obtiene los préstamos almacenados en la base de datos.

#### Ejemplo

```http
GET /prestamos
```

---

### GET /prestamos?impago=1

Obtiene los préstamos filtrados por impago.

#### Ejemplo

```http
GET /prestamos?impago=1
```

---

### GET /prestamos/<id>

Obtiene un préstamo concreto.

#### Ejemplo

```http
GET /prestamos/7
```

---

### GET /estadisticas

Obtiene estadísticas generales del conjunto de datos.

#### Respuesta

```json
{
    "total_prestamos": 51070,
    "prima_media": 385.29,
    "total_impagos": 59307
}
```

---

### POST /prestamos

Crea un nuevo préstamo.

#### Ejemplo de petición

```json
{
    "edad": 30,
    "ingresos": 25000,
    "monto_inicial": 15000
}
```

#### Respuesta

```json
{
    "mensaje": "Prestamo creado correctamente"
}
```

### PUT /prestamos/<row_id>
Actualiza un préstamo existente.