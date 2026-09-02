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

def obtener_todas_las_clases():
    """Obtiene la lista completa de clases registradas."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT id, materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive 
        FROM clases 
        ORDER BY CASE 
            WHEN dia_semana = 'Lunes' THEN 1
            WHEN dia_semana = 'Martes' THEN 2
            WHEN dia_semana = 'Miércoles' THEN 3
            WHEN dia_semana = 'Jueves' THEN 4
            WHEN dia_semana = 'Viernes' THEN 5
            WHEN dia_semana = 'Sábado' THEN 6
            WHEN dia_semana = 'Domingo' THEN 7
            ELSE 8 END, hora_inicio ASC
    """)
    
    clases = cursor.fetchall()
    conexion.close()
    return clases

def obtener_clases_por_dia(dia_semana):
    """Obtiene la lista de clases programadas para un día específico."""
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

def actualizar_clase(clase_id, materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive):
    """Actualiza la información de una clase existente."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        UPDATE clases
        SET materia = ?, grupo = ?, dia_semana = ?, hora_inicio = ?, hora_fin = ?, link_drive = ?
        WHERE id = ?
    """, (materia, grupo, dia_semana, hora_inicio, hora_fin, link_drive, clase_id))
    
    conexion.commit()
    conexion.close()
    print(f"Clase ID {clase_id} actualizada correctamente.")

def eliminar_clase(clase_id):
    """Elimina una clase de la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("DELETE FROM clases WHERE id = ?", (clase_id,))
    
    conexion.commit()
    conexion.close()
    print(f"Clase ID {clase_id} eliminada correctamente.")  
