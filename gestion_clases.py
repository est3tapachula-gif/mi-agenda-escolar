import sqlite3
from database import obtener_conexion

def agregar_clase(materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive=""):
    """Inserta una nueva clase en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        INSERT INTO clases (materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive))
    
    conexion.commit()
    conexion.close()
    print(f"Clase '{materia}' para el grupo {grupo} guardada exitosamente.")

def obtener_clases_por_dia(dia_semana):
    """Obtiene la lista de clases programadas para un día específico (ej. 'Lunes')."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT id, materia, grupo, hora_inicio, hora_fin, link_drive 
        FROM clases 
        WHERE dia_semana = ?
        ORDER BY hora_inicio ASC
    """, (dia_semana,))
    
    clases = cursor.fetchall()
    conexion.close()
    return clases

if __name__ == "__main__":
    # Prueba del módulo: Agregar una clase de ejemplo
    # Puedes cambiar estos datos por tus datos reales de la EST 3
    agregar_clase(
        materia="Español",
        grupo="2°G",
        dia_semana="Lunes",
        hora_inicio="08:00",
        hora_fin="08:50",
        link_drive="https://drive.google.com"
    )
    
    # Probar lectura de clases del Lunes
    print("\nClases del Lunes:")
    for clase in obtener_clases_por_dia("Lunes"):
        print(clase)
