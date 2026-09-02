import sqlite3
import webbrowser
from database import obtener_conexion

def guardar_actividades_sesion(clase_id, fecha, actividades_hoy, actividades_siguiente=""):
    """Guarda o actualiza el registro diario de actividades para una clase."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Comprobar si ya existe un registro para esta clase en esta fecha
    cursor.execute("""
        SELECT id FROM sesiones WHERE clase_id = ? AND fecha = ?
    """, (clase_id, fecha))
    
    registro = cursor.fetchone()
    
    if registro:
        # Actualizar la sesión existente
        cursor.execute("""
            UPDATE sesiones 
            SET actividades_hoy = ?, actividades_siguiente = ?
            WHERE id = ?
        """, (actividades_hoy, actividades_siguiente, registro[0]))
    else:
        # Insertar una nueva sesión
        cursor.execute("""
            INSERT INTO sesiones (clase_id, fecha, actividades_hoy, actividades_siguiente)
            VALUES (?, ?, ?, ?)
        """, (clase_id, fecha, actividades_hoy, actividades_siguiente))
        
    conexion.commit()
    conexion.close()
    print(f"Actividades para la clase ID {clase_id} guardadas correctamente.")

def abrir_lista_drive(url_drive):
    """Abre el enlace de Google Drive en el navegador web del sistema o dispositivo."""
    if url_drive:
        webbrowser.open(url_drive)
        print("Abriendo enlace de Google Drive...")
    else:
        print("No hay un enlace de Google Drive asignado a esta clase.")

if __name__ == "__main__":
    # Prueba del módulo: Guardar sesión de hoy y probar apertura de enlace
    guardar_actividades_sesion(
        clase_id=1,
        fecha="2026-09-02",
        actividades_hoy="Revisión de avances del proyecto y pase de lista.",
        actividades_siguiente="Presentación de rúbrica de evaluación."
    )
