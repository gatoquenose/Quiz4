import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

# =========================================
# 1. CONEXIÓN CON NEO4J
# =========================================

load_dotenv(override=True)

URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")


def correr(driver, query, **params):
    registros, _, _ = driver.execute_query(query, **params)
    return registros


# =========================================
# 2. CREACIÓN DE NODOS Y RELACIONES
# =========================================

def cargar_datos(driver):

    estudiantes = [
        ("Ana", "Computadores"),
        ("Luis", "Computadores"),
        ("María", "Electrónica"),
        ("Diego", "Computadores"),
        ("Sofía", "Electrónica"),
        ("Carlos", "Mecatrónica")
    ]

    cursos = [
        ("CE2103", "Algoritmos y Estructuras de Datos II"),
        ("EL2207", "Elementos Activos"),
        ("FI1202", "Física General II")
    ]

    amistades = [
        ("Ana", "Luis"),
        ("Luis", "Diego"),
        ("Ana", "María"),
        ("María", "Sofía"),
        ("Sofía", "Carlos")
    ]

    matriculas = [
        ("Ana", "CE2103"),
        ("Luis", "CE2103"),
        ("Diego", "CE2103"),
        ("Ana", "FI1202"),
        ("María", "FI1202"),
        ("Sofía", "EL2207"),
        ("María", "EL2207"),
        ("Carlos", "FI1202")
    ]

    # Crear estudiantes
    for nombre, carrera in estudiantes:
        correr(driver, """
            MERGE (e:Estudiante {nombre: $nombre})
            SET e.carrera = $carrera
        """, nombre=nombre, carrera=carrera)

    # Crear cursos
    for codigo, nombre in cursos:
        correr(driver, """
            MERGE (c:Curso {codigo: $codigo})
            SET c.nombre = $nombre
        """, codigo=codigo, nombre=nombre)

    # Crear relaciones de amistad
    for a, b in amistades:
        correr(driver, """
            MATCH (x:Estudiante {nombre: $a})
            MATCH (y:Estudiante {nombre: $b})
            MERGE (x)-[:AMIGO_DE]->(y)
        """, a=a, b=b)

    # Crear relaciones de matrícula
    for estudiante, codigo in matriculas:
        correr(driver, """
            MATCH (e:Estudiante {nombre: $estudiante})
            MATCH (c:Curso {codigo: $codigo})
            MERGE (e)-[:MATRICULADO_EN]->(c)
        """, estudiante=estudiante, codigo=codigo)

    print("¡Datos cargados correctamente!")


# =========================================
# 3. RECOMENDAR AMIGOS
# =========================================

def recomendar_amigos(driver, nombre):
    return correr(driver, """
        MATCH (yo:Estudiante {nombre: $nombre})
            -[:AMIGO_DE]-(amigo:Estudiante)
            -[:AMIGO_DE]-(rec:Estudiante)
        WHERE rec <> yo
        AND NOT EXISTS {
            MATCH (yo)-[:AMIGO_DE]-(rec)
        }
        RETURN rec.nombre AS nombre,
            count(DISTINCT amigo) AS en_comun
        ORDER BY en_comun DESC, nombre
    """, nombre=nombre)


# =========================================
# 4. CAMINO MÁS CORTO ENTRE ESTUDIANTES
# =========================================

def camino_mas_corto(driver, a, b):
    return correr(driver, """
        MATCH p = shortestPath(
            (x:Estudiante {nombre: $a})
            -[:AMIGO_DE*]-
            (y:Estudiante {nombre: $b})
        )
        RETURN [n IN nodes(p) | n.nombre] AS camino
    """, a=a, b=b)


# =========================================
# 5. COMPAÑEROS DE CURSO
# =========================================

def companeros_de_curso(driver, nombre):
    return correr(driver, """
        MATCH (yo:Estudiante {nombre: $nombre})
            -[:MATRICULADO_EN]->(c:Curso)
            <-[:MATRICULADO_EN]-(otro:Estudiante)
        WHERE otro <> yo
        RETURN otro.nombre AS nombre,
            collect(c.codigo) AS cursos
        ORDER BY nombre
    """, nombre=nombre)


# =========================================
# 6. PROGRAMA PRINCIPAL
# =========================================

def main():
    if not URI or not USER or not PASSWORD:
        print("Faltan credenciales en el archivo .env")
        return

    try:
        with GraphDatabase.driver(
            URI, auth=(USER, PASSWORD)
        ) as driver:

            driver.verify_connectivity()
            print("¡Conexión exitosa con Neo4j!")

            cargar_datos(driver)

            print("\nRECOMENDACIONES PARA ANA:")
            for r in recomendar_amigos(driver, "Ana"):
                print(
                    f"{r['nombre']}: "
                    f"{r['en_comun']} amigo(s) en común"
                )

            print("\nCAMINO MÁS CORTO ANA -> CARLOS:")
            for r in camino_mas_corto(driver, "Ana", "Carlos"):
                print(" -> ".join(r["camino"]))

            print("\nCOMPAÑEROS DE CURSO DE ANA:")
            for r in companeros_de_curso(driver, "Ana"):
                print(
                    f"{r['nombre']}: "
                    f"{', '.join(r['cursos'])}"
                )

    except Exception as error:
        print("Ocurrió un error:")
        print(error)


if __name__ == "__main__":
    main()
