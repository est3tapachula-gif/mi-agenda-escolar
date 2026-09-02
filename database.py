import sqlite3

def obtener_conexion():
    """Crea o se conecta a la base de datos local de la agenda."""
    return sqlite3.connect("agenda_escolar.db")

def inicializar_db():
    """Crea las tablas necesarias para guardar las 'fichas' de clases, sesiones y tareas."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # 1. Tabla de Clases (Materia, Grupo, Horario habitual y Enlace a Drive)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        materia TEXT NOT NULL,
        grupo TEXT NOT NULL,
        dia_semana TEXT NOT NULL,  -- Ej: 'Lunes', 'Martes', etc.
        hora_inicio TEXT NOT NULL, -- Ej: '08:00'
        hora_fin TEXT NOT NULL,    -- Ej: '08:50'
        link_drive TEXT            -- Enlace a las listas/documentos en Google Drive
    )
    """)

    # 2. Tabla de Sesiones Diarias (Registro de actividades por clase)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sesiones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clase_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,               -- Fecha en formato YYYY-MM-DD
        actividades_hoy TEXT,               -- Lo que se trabajó en el día
        actividades_siguiente TEXT,         -- Plan para la siguiente sesión
        FOREIGN KEY(clase_id) REFERENCES clases(id)
    )
    """)

    # 3. Tabla de Tareas y Avisos Programados
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        descripcion TEXT,
        fecha_hora TEXT NOT NULL,          -- Fecha y hora para la notificación
        estatus TEXT DEFAULT 'pendiente'   -- 'pendiente' o 'completada'
    )
    """)

    conexion.commit()
    conexion.close()
    print("Base de datos e infraestructura de fichas lista correctamente.")

if __name__ == "__main__":
    # Al ejecutar este script directamente, se crea o verifica la base de datos
    inicializar_db()
