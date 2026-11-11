# Quiz #4 – Base de Datos NoSQL: Grafos

**Instituto Tecnológico de Costa Rica**

**Curso:** Algoritmos y Estructuras de Datos II (CE2103)

**II Semestre 2026**

## 1. Descripción del proyecto

Este proyecto consiste en desarrollar un pequeño sistema de relaciones universitarias utilizando Python y una base de datos NoSQL orientada a grafos, implementada mediante Neo4j.

El programa representa una red de estudiantes que tienen relaciones de amistad y se encuentran matriculados en diferentes cursos. A partir de estas conexiones, es posible consultar información sobre los estudiantes y analizar las relaciones existentes entre ellos.

## 2. Contexto del problema

En un entorno universitario, los estudiantes pueden conocer a diferentes personas y compartir cursos con otros compañeros. Sin embargo, identificar estas conexiones puede resultar complicado cuando existen múltiples relaciones entre estudiantes.

Para ejemplificar esta situación, se desarrolló un sistema que permite recomendar nuevas amistades, encontrar el camino más corto entre dos estudiantes y determinar cuáles compañeros comparten cursos.

## 3. Implementación de la base de datos NoSQL

Se utilizó Neo4j, una base de datos orientada a grafos, debido a que permite representar la información mediante nodos y relaciones.

El modelo desarrollado contiene dos tipos de nodos:

- **Estudiante:** almacena el nombre y la carrera de cada estudiante.
- **Curso:** almacena el código y el nombre de cada curso.

Además, se implementaron dos tipos de relaciones:

- **AMIGO_DE:** representa una amistad entre dos estudiantes.
- **MATRICULADO_EN:** relaciona a un estudiante con un curso.

Para crear y consultar estos elementos se utilizó el lenguaje Cypher, ejecutando las consultas directamente desde Python mediante la biblioteca oficial de Neo4j.

## 4. Funcionalidades del programa

**Recomendación de amistades:** identifica estudiantes que tienen amigos en común, pero que todavía no poseen una relación directa de amistad.

**Camino más corto:** utiliza la función `shortestPath()` de Neo4j para determinar la ruta con menos relaciones de amistad entre dos estudiantes.

**Compañeros de curso:** consulta cuáles estudiantes están matriculados en los mismos cursos que una persona determinada.

## 5. Datos utilizados

Para demostrar el funcionamiento del sistema se crearon seis estudiantes y tres cursos universitarios.

Se establecieron cinco relaciones de amistad y ocho relaciones de matrícula, obteniendo un grafo de nueve nodos y trece relaciones.

## 6. Tecnologías utilizadas

- Python: desarrollo del programa.
- Neo4j AuraDB: almacenamiento de los nodos y sus relaciones.
- Cypher: creación y consulta de los grafos.
- Biblioteca `neo4j`: conexión entre Python y la base de datos.
- Biblioteca `python-dotenv`: lectura de las variables de entorno.

## 7. Ejecución del programa

Para ejecutar el proyecto se necesita Python y acceso a una instancia de Neo4j.

Primero, se deben instalar las bibliotecas necesarias mediante el archivo `requirements.txt`:

`pip install -r requirements.txt`

Después, se debe crear un archivo `.env` con las variables `NEO4J_URI`, `NEO4J_USER` y `NEO4J_PASSWORD`, utilizando las credenciales de la instancia de Neo4j.

Finalmente, se ejecuta:

`python main.py`

El programa cargará los datos de ejemplo y mostrará las recomendaciones de amistad, el camino más corto y los compañeros de curso de Ana.

## 8. Conclusión

Mediante este proyecto se logró implementar una base de datos NoSQL orientada a grafos y utilizarla desde un programa desarrollado en Python.

El uso de Neo4j permitió representar las conexiones entre estudiantes y cursos de una forma sencilla. Además, se demostró cómo las consultas sobre grafos permiten obtener información relacionada con amistades, matrículas y caminos entre diferentes nodos.