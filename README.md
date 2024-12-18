
# Sistema de Recomendación de Películas TMDb

Entrega final de mi proyecto para la carrera de Tecnicatura Universitaria en Programación de UTN-FRA.
Este proyecto implementa un sistema de recomendación de películas utilizando **Clustering no supervisado** y **Random Forest**, además de una interfaz interactiva con **Streamlit**. El sistema está diseñado para recomendar una película similar a partir de un título ingresado por el usuario y permite registrar feedback para mejorar el modelo.

---

## **Características del Proyecto**

- **Recomendación de Películas**: Utiliza **Agglomerative Clustering** para encontrar películas similares.
- **Feedback del Usuario**: El feedback ("buena" o "mala") se almacena en una base de datos MySQL.
- **Modelo Random Forest**: Aprende del feedback del usuario para ajustar las recomendaciones.
- **Interfaz Web**: Implementada con **Streamlit** para una experiencia de usuario sencilla e interactiva.

---

## **Requisitos**

1. Python 3.8 o superior.
2. Servidor MySQL (para la base de datos).

### **Instalación de Dependencias**

Ejecuta el siguiente comando para instalar todas las dependencias necesarias:
```bash
pip install -r requirements.txt
```

---

## **Configuración de la Base de Datos**

### **1. Crear la base de datos y tablas**

```sql
CREATE DATABASE recomendador_peliculas;
USE recomendador_peliculas;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    pelicula_ingresada VARCHAR(255) NOT NULL,
    pelicula_recomendada VARCHAR(255) NOT NULL,
    feedback VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES usuarios(id)
);
```

### **2. Configurar la conexión a MySQL**
Edita el archivo `database/db_connection.py` con los detalles de tu servidor MySQL:
```python
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # Cambia por tu usuario de MySQL
        password="password", # Cambia por tu contraseña
        database="recomendador_peliculas"
    )
```

---

## **Estructura del Proyecto**

```plaintext
recomendador_peliculas/
|
├── data/                          # Datos crudos y procesados
│   ├── tmdb_2023_movies.csv       # Dataset original de TMDb
│   └── feedback.db                # Archivo SQLite opcional
|
├── database/                      # Scripts y conexión a la base de datos
│   └── db_connection.py           # Conexión a MySQL
|
├── models/                        # Modelos de machine learning
│   ├── clustering_model.py        # Clustering Agglomerative
│   └── random_forest_model.py     # Modelo Random Forest
|
├── scripts/                       # Scripts auxiliares
│   ├── preprocessing.py           # Procesamiento del dataset
│   └── feedback_handler.py        # Guardar y cargar feedback
|
├── app/                           # Aplicación principal
│   ├── main.py                    # Streamlit principal
│   └── recommend.py               # Lógica de recomendación
|
├── tests/                         # Pruebas unitarias
├── .gitignore                     # Archivos ignorados por Git
├── requirements.txt               # Dependencias
└── README.md                      # Documentación
```

---

## **Ejecución del Proyecto**

1. **Iniciar la base de datos**
2. **Cargar el dataset**: Guarda el archivo `tmdb_2023_movies.csv` en la carpeta `data/`.
3. **Ejecutar la aplicación**:

```bash
streamlit run app/main.py
```

---

## **Uso de la Aplicación**

1. **Recomendación Inicial**: Ingresa el título de una película.
2. **Feedback**: Califica la recomendación como "buena" o "mala".
3. **Retroalimentación Continua**: Los datos de feedback se almacenan en la base de datos para reentrenar el modelo Random Forest.

---

## **Próximos Pasos**

- Implementar un modelo **híbrido** que combine clustering y filtrado colaborativo.
- Mejorar la interfaz de usuario con Streamlit.

---

## **Autor**
- **Nombre**: [Morales Mauro]
- **Contacto**: [moralesmaurot6@gmail.com]
