import sqlite3
from database import obtener_conexion

def guardar_actividades_sesion(clase_id, fecha, actividades_hoy, actividades_siguiente=""):
    """Guarda o actualiza el registro diario de actividades para una clase."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT id FROM sesiones WHERE clase_id = ? AND fecha = ?
    """, (clase_id, fecha))
    
    registro = cursor.fetchone()
    
    if registro:
        cursor.execute("""
            UPDATE sesiones 
            SET actividades_hoy = ?, actividades_siguiente = ?
            WHERE id = ?
        """, (actividades_hoy, actividades_siguiente, registro[0]))
    else:
        cursor.execute("""
            INSERT INTO sesiones (clase_id, fecha, actividades_hoy, actividades_siguiente)
            VALUES (?, ?, ?, ?)
        """, (clase_id, fecha, actividades_hoy, actividades_siguiente))
        
    conexion.commit()
    conexion.close()

def obtener_actividad_sesion(clase_id, fecha):
    """Obtiene el registro de actividades guardado para una clase en una fecha específica."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    cursor.execute("""
        SELECT actividades_hoy, actividades_siguiente 
        FROM sesiones 
        WHERE clase_id = ? AND fecha = ?
    """, (clase_id, fecha))
    
    resultado = cursor.fetchone()
    conexion.close()
    
    if resultado:
        return resultado[0] or "", resultado[1] or ""
    return "", ""
