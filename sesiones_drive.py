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

def obtener_actividad_sesion(clase_id, fecha, grupo=None):
    """
    Obtiene las actividades de la sesión. Si está en blanco, busca la última 
    nota guardada en 'actividades_siguiente' de cualquier sesión previa del mismo grupo.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # 1. Buscar si esta sesión específica ya tiene datos guardados
    cursor.execute("""
        SELECT actividades_hoy, actividades_siguiente 
        FROM sesiones 
        WHERE clase_id = ? AND fecha = ?
    """, (clase_id, fecha))
    
    resultado = cursor.fetchone()
    
    act_hoy = resultado[0] if resultado and resultado[0] else ""
    act_sig = resultado[1] if resultado and resultado[1] else ""
    
    # 2. Si el campo 'actividades_hoy' está vacío, traer lo planeado en la sesión anterior del grupo
    if not act_hoy and grupo:
        cursor.execute("""
            SELECT s.actividades_siguiente 
            FROM sesiones s
            JOIN clases c ON s.clase_id = c.id
            WHERE c.grupo = ? 
              AND s.clase_id != ?
              AND s.actividades_siguiente IS NOT NULL 
              AND s.actividades_siguiente != ''
            ORDER BY s.id DESC
            LIMIT 1
        """, (grupo, clase_id))
        
        ultima_nota = cursor.fetchone()
        if ultima_nota and ultima_nota[0]:
            act_hoy = ultima_nota[0]
            
    conexion.close()
    return act_hoy, act_sig
