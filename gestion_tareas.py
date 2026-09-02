import sqlite3
from database import obtener_conexion

def asegurar_tabla_tareas():
    """Asegura que la tabla de tareas exista con la estructura correcta."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT,
            fecha_hora TEXT NOT NULL,
            estado TEXT DEFAULT 'pendiente'
        )
    """)
    conexion.commit()
    conexion.close()

def agregar_tarea(titulo, descripcion, fecha_hora):
    """Agrega una nueva tarea o aviso."""
    asegurar_tabla_tareas()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO tareas (titulo, descripcion, fecha_hora, estado)
        VALUES (?, ?, ?, 'pendiente')
    """, (titulo, descripcion, fecha_hora))
    conexion.commit()
    conexion.close()

def obtener_tareas_pendientes():
    """Obtiene todas las tareas con estado pendiente."""
    asegurar_tabla_tareas()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT id, titulo, descripcion, fecha_hora 
        FROM tareas 
        WHERE estado = 'pendiente'
        ORDER BY fecha_hora ASC
    """)
    tareas = cursor.fetchall()
    conexion.close()
    return tareas

def marcar_tarea_completada(tarea_id):
    """Marca una tarea como completada."""
    asegurar_tabla_tareas()
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        UPDATE tareas 
        SET estado = 'completada' 
        WHERE id = ?
    """, (tarea_id,))
    conexion.commit()
    conexion.close()
