import sqlite3
from database import obtener_conexion

def agregar_tarea(titulo, descripcion, fecha_hora):
    """Guarda una nueva tarea o aviso programado en la base de datos."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        INSERT INTO tareas (titulo, descripcion, fecha_hora, estatus)
        VALUES (?, ?, ?, 'pendiente')
    """, (titulo, descripcion, fecha_hora))
    
    conexion.commit()
    conexion.close()
    print(f"Tarea '{titulo}' programada para {fecha_hora}.")

def obtener_tareas_pendientes():
    """Obtiene la lista de tareas que están pendientes."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT id, titulo, descripcion, fecha_hora 
        FROM tareas 
        WHERE estatus = 'pendiente'
        ORDER BY fecha_hora ASC
    """)
    
    tareas = cursor.fetchall()
    conexion.close()
    return tareas

def marcar_tarea_completada(tarea_id):
    """Cambia el estado de una tarea a completada."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        UPDATE tareas 
        SET estatus = 'completada'
        WHERE id = ?
    """, (tarea_id,))
    
    conexion.commit()
    conexion.close()
    print(f"Tarea ID {tarea_id} marcada como completada.")

if __name__ == "__main__":
    # Prueba del módulo: Agregar un aviso de prueba
    agregar_tarea(
        titulo="Entregar reporte de evaluación",
        descripcion="Subir lista de cotejo a la dirección.",
        fecha_hora="2026-09-05 14:00"
    )
    
    print("\nTareas pendientes:")
    for tarea in obtener_tareas_pendientes():
        print(tarea)
